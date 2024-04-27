from functools import lru_cache

from pydantic_settings import BaseSettings


@lru_cache()
def get_settings() -> BaseSettings:
    return Settings()


class Settings(BaseSettings):
    # ETL
    table_name: str

    # Gcp
    gcp_credentials_path: str
    gcp_project_name: str
    bq_dataset_name: str

    gcs_bucket_name: str

    # Aws
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str

    s3_bucket_name: str

    redshift_host: str
    redshift_port: int
    redshift_database: str
    redshift_cluster: str
    redshift_master_username: str
    redshift_master_password: str
