from airflow.decorators import task_group
from airflow.models.baseoperator import chain
from connections import create_connection
from settings import GCP_CONN_ID, GCP_CREDENTIALS_PATH
from transfer_gcs_to_bq import transfer_gcs_to_bq
from upload import upload


@task_group
def gcp_pipeline_group() -> None:
    """Google Cloud Platform Pipeline

    Returns:
        None
    """

    connection = create_connection.override(task_id="gcp_connection")(
        connection_id=GCP_CONN_ID,
        connection_type="google_cloud_platform",
        extra={"key_path": GCP_CREDENTIALS_PATH},
    )

    transfer = transfer_gcs_to_bq()

    chain(connection, upload(), transfer)
