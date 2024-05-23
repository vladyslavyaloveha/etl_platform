import logging
from enum import Enum
from pathlib import Path

from airflow.decorators import task
from airflow.operators.python import get_current_context

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
    cloud_provider = context["params"].get("CLOUD_PROVIDER")
    task_instance = context["task_instance"]
    analytics_file_path = task_instance.xcom_pull(
        task_ids="extract_data", key="analytics_file_path"
    )

    key = Path(analytics_file_path).name

    logger.info(
        f"Start pipeline for file_path: {analytics_file_path}, cloud provider: {cloud_provider}"
    )

    task_instance.xcom_push(key="file_path", value=analytics_file_path)
    task_instance.xcom_push(key="cloud_provider", value=cloud_provider)
    task_instance.xcom_push(key="file_key", value=key)

    match cloud_provider:
        case CloudProviders.AWS:
            return "aws_pipeline_group.aws_connection"
        case CloudProviders.GCP:
            return "gcp_pipeline_group.gcp_connection"
