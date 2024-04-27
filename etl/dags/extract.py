import datetime
import logging
import pathlib
import uuid
from typing import Final

import requests
from airflow.decorators import task
from airflow.operators.python import get_current_context
from settings import BASE_DIRECTORY

logger = logging.getLogger("airflow.task")

MAX_RETRIES: Final[int] = 3
RETRY_DELAY: Final[int] = 2

RESPONSE_CHUNK_SIZE: Final[int] = 512


@task(
    task_id="extract_data",
    retries=MAX_RETRIES,
    retry_delay=datetime.timedelta(seconds=RETRY_DELAY),
    retry_exponential_backoff=True,
)
def extract() -> None:
    """Extracts data in .parquet format from given url
    Returns:
        None
    """

    context = get_current_context()
    file_url = context["params"].get("FILE_URL")

    file_path = str(
        pathlib.Path(BASE_DIRECTORY)
        .joinpath(f"{pathlib.Path(file_url).name}.{str(uuid.uuid4())[:8]}")
        .resolve()
    )

    logger.info(f"started extract data from {file_url} to {str(file_path)}")

    with requests.Session() as session:
        with session.get(file_url, stream=True) as response:
            response.raise_for_status()
            with open(file_path, mode="wb") as file:
                logger.info(f"started write data to {file.name} file")
                for chunk in response.iter_content(chunk_size=RESPONSE_CHUNK_SIZE):
                    file.write(chunk)
                logger.info(f"end write data to {file.name} file")

    task_instance = context["task_instance"]
    task_instance.xcom_push(key="file_path", value=file_path)

    logger.info(f"finished extract data from {file_url} to {str(file_path)}")
