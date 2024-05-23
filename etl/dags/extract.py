import asyncio
import datetime
import logging
import pathlib
from pathlib import Path

import httpx
import pandas as pd
from airflow.decorators import task
from airflow.operators.python import get_current_context
from settings import (
    BASE_DIRECTORY,
    BASE_URL,
    MAX_RETRIES,
    RESPONSE_CHUNK_SIZE,
    RETRY_DELAY,
)

logger = logging.getLogger("airflow.task")


async def extract_file(client: httpx.AsyncClient, file_url: str) -> str | None:
    """Extracts and writes file from provided url

    Args:
        client (httpx.AsyncClient): Httpx async client instance
        file_url (str): file url
    Returns:
        str | None: path to file or None
    """
    file_path = str(
        pathlib.Path(BASE_DIRECTORY)
        .joinpath(f"{pathlib.Path(file_url).name}")
        .resolve()
    )
    async with client.stream("GET", file_url) as response:
        if response.status_code != 200:
            logger.warning(f"Response {response.status_code}: {file_path}")
            return None
        with open(file_path, mode="wb") as file:
            logger.info(f"started write data to {file.name} file")
            async for chunk in response.aiter_bytes(chunk_size=RESPONSE_CHUNK_SIZE):
                file.write(chunk)
    return file_path


async def extract_files(file_urls: list[str]) -> list[str]:
    """Extracts and writes files from provided list of urls

    Args:
        file_urls (list[str]): List of files urls
    Returns:
        list[str]: list of file paths
    """
    async with httpx.AsyncClient() as client:
        tasks = [extract_file(client, url) for url in file_urls]
        result = await asyncio.gather(*tasks)
        return list(filter(lambda file_path: file_path is not None, result))


@task(
    task_id="extract_data",
    retries=MAX_RETRIES,
    retry_delay=datetime.timedelta(seconds=RETRY_DELAY),
    retry_exponential_backoff=True,
)
def extract() -> None:
    """Extracts data in .parquet format for provided date range

    Returns:
        None
    """

    context = get_current_context()
    start_date = datetime.datetime.strptime(
        context["params"].get("start_date"), "%Y-%m-%d"
    )
    end_date = datetime.datetime.strptime(context["params"].get("end_date"), "%Y-%m-%d")

    date_range = (
        pd.date_range(start_date, end_date, freq="m").strftime("%Y-%m").tolist()
    )
    file_urls = [f"{BASE_URL}/yellow_tripdata_{date_}.parquet" for date_ in date_range]

    logger.info(f"Generated {len(file_urls)} files urls to get trip data: {file_urls}")
    logger.info("started extract data")

    file_paths = asyncio.run(extract_files(file_urls))

    if not file_paths:
        raise ValueError("Files are not extracted")

    analytics_file_path = str(
        Path(file_paths[0])
        .parent.joinpath(
            f"analytics-{start_date.strftime('%Y-%m').replace('-', '')}-{end_date.strftime('%Y-%m').replace('-', '')}.parquet"
        )
        .resolve()
    )

    task_instance = context["task_instance"]
    task_instance.xcom_push(key="file_paths", value=file_paths)
    task_instance.xcom_push(key="analytics_file_path", value=analytics_file_path)

    logger.info("finished extract data from")
