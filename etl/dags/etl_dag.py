import logging
import pathlib
from datetime import timedelta

import pendulum
from airflow.decorators import dag
from airflow.models import Param
from airflow.models.baseoperator import chain
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from aws import aws_pipeline_group
from branch import CloudProviders, branch_task
from connections import create_connection
from extract import extract
from gcp import gcp_pipeline_group
from settings import (
    BASE_DIRECTORY,
    DAG_RUN_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
    SPARK_CONN_ID,
    SPARK_MASTER_URL,
)

logger = logging.getLogger("airflow.dag")


@dag(
    dag_id="ETL_trip_data",
    start_date=pendulum.today(tz="UTC"),
    description="ETL trip data pipeline. Extracts data in .parquet format,"
    "transforms, loads to storage and transfers from storage to database",
    params={
        "start_date": Param(
            title="Start date",
            description="Provide start date for receiving data",
            default="2024-01-01",
            type="string",
            format="date",
            min_length=10,
            max_length=10,
        ),
        "end_date": Param(
            title="End date",
            description="Provide end date for receiving data",
            default="2024-05-01",
            type="string",
            format="date",
            min_length=10,
            max_length=10,
        ),
        "CLOUD_PROVIDER": Param(
            title="Cloud provider",
            description="Select cloud provider",
            enum=[CloudProviders.AWS, CloudProviders.GCP],
            default=CloudProviders.GCP,
        ),
    },
    schedule=None,
    catchup=False,
    dagrun_timeout=timedelta(seconds=DAG_RUN_TIMEOUT),
    tags=["pipeline", "gcp", "aws"],
)
def Pipeline() -> None:
    """ETL trip data pipeline"""

    extract_data = extract

    spark_connection = create_connection.override(task_id="spark_connection")(
        connection_id=SPARK_CONN_ID, connection_type="spark", host=SPARK_MASTER_URL
    )

    spark_submit_job = SparkSubmitOperator(
        task_id="analytics_transform_job",
        retries=MAX_RETRIES,
        retry_delay=timedelta(seconds=RETRY_DELAY),
        retry_exponential_backoff=True,
        application=str(
            pathlib.Path(BASE_DIRECTORY).parent.joinpath("transform.py").resolve()
        ),
        conn_id=SPARK_CONN_ID,
        application_args=[
            "{{ti.xcom_pull(task_ids='extract_data', key='file_paths')}}",
            "{{ti.xcom_pull(task_ids='extract_data', key='analytics_file_path')}}",
        ],
    )

    chain(
        extract_data(),
        spark_connection,
        spark_submit_job,
        branch_task(),
        [aws_pipeline_group(), gcp_pipeline_group()],
    )


dag = Pipeline()
