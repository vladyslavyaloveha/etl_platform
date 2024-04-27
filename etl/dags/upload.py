import logging
import pathlib

from airflow.decorators import task
from airflow.operators.python import get_current_context
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from branch import CloudProviders
from settings import AWS_CONN_ID, GCP_CONN_ID, GCS_BUCKET_NAME, S3_BUCKET_NAME

logger = logging.getLogger("airflow.task")


@task
def upload() -> None:
    """Uploads aggregated .parquet file to Cloud Provider Storage (Google Cloud Storage or S3)

    Returns:
        None
    """

    task_instance = get_current_context()["task_instance"]

    path = pathlib.Path(
        task_instance.xcom_pull(task_ids="extract_data", key="file_path")
    )
    cloud_provider = task_instance.xcom_pull(
        task_ids="branch_task", key="cloud_provider"
    )

    key = task_instance.xcom_pull(task_ids="branch_task", key="file_key")
    file_path = str(path.parent.joinpath(key).resolve())

    logger.info(f"started upload data to {cloud_provider} from {file_path}")

    match cloud_provider:
        case CloudProviders.AWS:
            hook = S3Hook(aws_conn_id=AWS_CONN_ID)
            hook.load_file(
                filename=file_path, key=key, bucket_name=S3_BUCKET_NAME, replace=True
            )
        case CloudProviders.GCP:
            hook = GCSHook(gcp_conn_id=GCP_CONN_ID)
            hook.upload(
                bucket_name=GCS_BUCKET_NAME,
                object_name=key,
                filename=file_path,
            )

    logger.info(f"finished upload data, bucket: {GCS_BUCKET_NAME}, key: {key}")
