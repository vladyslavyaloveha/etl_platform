import logging

from airflow.decorators import task
from airflow.operators.python import get_current_context
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from settings import (
    BQ_DATASET_NAME,
    GCP_CONN_ID,
    GCP_PROJECT_NAME,
    GCS_BUCKET_NAME,
    TABLE_NAME,
)

logger = logging.getLogger("airflow.task")

JOB_CONFIG: dict[str] = {
    "load": {
        "destinationTable": {
            "projectId": GCP_PROJECT_NAME,
            "datasetId": BQ_DATASET_NAME,
            "tableId": TABLE_NAME,
        },
        "sourceFormat": "PARQUET",
        "writeDisposition": "WRITE_TRUNCATE",
        "autodetect": True,
    },
}


@task
def transfer_gcs_to_bq() -> None:
    """Transfer data from Google Cloud Storage to BigQuery

    Returns:
        None
    """

    task_instance = get_current_context()["task_instance"]
    key = task_instance.xcom_pull(task_ids="branch_task", key="file_key")

    logger.info(f"started data transfer for key: {key}")

    JOB_CONFIG["load"]["sourceUris"] = [f"gs://{GCS_BUCKET_NAME}/{key}"]
    hook = BigQueryHook(gcp_conn_id=GCP_CONN_ID)
    hook.insert_job(
        configuration=JOB_CONFIG,
        project_id=GCP_PROJECT_NAME,
    )

    logger.info(f"finished data transfer for key: {key}")
