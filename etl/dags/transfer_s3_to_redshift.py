import logging

from airflow.decorators import task, task_group
from airflow.models.baseoperator import chain
from airflow.providers.amazon.aws.hooks.redshift_data import RedshiftDataHook
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from connections import create_connection
from settings import (
    AWS_CONN_ID,
    AWS_REGION,
    REDSHIFT_CLUSTER,
    REDSHIFT_CONN_ID,
    REDSHIFT_DATABASE,
    REDSHIFT_HOST,
    REDSHIFT_MASTER_PASSWORD,
    REDSHIFT_MASTER_USERNAME,
    REDSHIFT_PORT,
    S3_BUCKET_NAME,
    TABLE_NAME,
)

logger = logging.getLogger("airflow.task")


@task
def create_redshift_table() -> None:
    """Creates Redshift table on Aws
    Returns:
        None
    """
    hook = RedshiftDataHook(aws_conn_id=AWS_CONN_ID, region_name=AWS_REGION)
    hook.execute_query(
        cluster_identifier=REDSHIFT_CLUSTER,
        database=REDSHIFT_DATABASE,
        sql=f"""CREATE TABLE IF NOT EXISTS public.{TABLE_NAME}(
                date DATE,
                passengers INTEGER,
                distance FLOAT,
                max_trip_distance FLOAT,
                uuid CHAR(36)
            );""",
    )


@task_group
def transfer_s3_to_redshift() -> None:
    """Transfer data from S3 to Redshift

    Returns:
        None
    """

    redshitft_connection = create_connection.override(task_id="redshift_connection")(
        connection_id=REDSHIFT_CONN_ID,
        connection_type="redshift",
        host=REDSHIFT_HOST,
        port=REDSHIFT_PORT,
        login=REDSHIFT_MASTER_USERNAME,
        password=REDSHIFT_MASTER_PASSWORD,
        schema=REDSHIFT_DATABASE,
    )

    transfer_s3_to_redshift = S3ToRedshiftOperator(
        task_id="transfer_s3_to_redshift",
        aws_conn_id=AWS_CONN_ID,
        redshift_conn_id=REDSHIFT_CONN_ID,
        s3_bucket=S3_BUCKET_NAME,
        s3_key="{{ti.xcom_pull(task_ids='branch_task', key='file_key')}}",
        schema="PUBLIC",
        table=TABLE_NAME,
        method="UPSERT",
        upsert_keys=["date", "passengers", "distance", "max_trip_distance"],
        copy_options=["parquet"],
    )

    logger.info("started data transfer")

    chain(redshitft_connection, create_redshift_table(), transfer_s3_to_redshift)

    logger.info("finished data transfer")
