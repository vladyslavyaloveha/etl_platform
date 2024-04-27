from airflow.decorators import task_group
from airflow.models.baseoperator import chain
from connections import create_connection
from settings import AWS_ACCESS_KEY_ID, AWS_CONN_ID, AWS_SECRET_ACCESS_KEY
from transfer_s3_to_redshift import transfer_s3_to_redshift
from upload import upload


@task_group
def aws_pipeline_group() -> None:
    """Amazon Web Services Pipeline

    Returns:
        None
    """

    connection = create_connection.override(task_id="aws_connection")(
        connection_id=AWS_CONN_ID,
        connection_type="aws",
        login=AWS_ACCESS_KEY_ID,
        password=AWS_SECRET_ACCESS_KEY,
    )

    transfer = transfer_s3_to_redshift()

    chain(connection, upload(), transfer)
