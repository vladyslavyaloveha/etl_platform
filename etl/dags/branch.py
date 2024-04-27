import logging
import pathlib
from enum import Enum

from airflow.decorators import task
from airflow.operators.python import get_current_context
from settings import BASE_DIRECTORY

logger = logging.getLogger("airflow.dag")


class CloudProviders(str, Enum):
    GCP = "Google Cloud Platform"
    AWS = "Amazon Web Services"


@task.branch(task_id="branch_task")
def branch_task() -> str:
    """Provides Pipeline execution selection based on passed Cloud Provider

    Returns:
        str: pipeline task_id
    """
    context = get_current_context()
    file_url = context["params"].get("FILE_URL")
    cloud_provider = context["params"].get("CLOUD_PROVIDER")

    file_path = (
        pathlib.Path(BASE_DIRECTORY).joinpath(pathlib.Path(file_url).name).resolve()
    )
    key = f"analytics_{file_path.name}"
    file_path = str(file_path)

    logger.info(
        f"Start pipeline for file_path: {file_path}, cloud provider: {cloud_provider}"
    )

    task_instance = context["task_instance"]
    task_instance.xcom_push(key="file_path", value=file_path)
    task_instance.xcom_push(key="file_url", value=file_url)
    task_instance.xcom_push(key="cloud_provider", value=cloud_provider)
    task_instance.xcom_push(key="file_key", value=key)

    match cloud_provider:
        case CloudProviders.AWS:
            return "aws_pipeline_group.aws_connection"
        case CloudProviders.GCP:
            return "gcp_pipeline_group.gcp_connection"
