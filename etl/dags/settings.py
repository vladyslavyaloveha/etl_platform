import os.path
from typing import Final

DAG_RUN_TIMEOUT: Final[int] = 60 * 10

FILE_URL: Final[str] = (
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
)

BASE_DIRECTORY = "/opt/airflow/dags/data"

TABLE_NAME: Final[str] = os.getenv("TABLE_NAME")

# Spark
SPARK_CONN_ID: Final[str] = "spark"
SPARK_MASTER_URL: Final[str] = os.getenv("SPARK_MASTER_URL")

# Gcp
GCP_CONN_ID: Final[str] = "google_cloud_platform"
GCP_CREDENTIALS_PATH: Final[str] = os.getenv("GCP_CREDENTIALS_PATH")
GCP_PROJECT_NAME: Final[str] = os.getenv("GCP_PROJECT_NAME")
BQ_DATASET_NAME: Final[str] = os.getenv("BQ_DATASET_NAME")

GCS_BUCKET_NAME: Final[str] = os.getenv("GCS_BUCKET_NAME")

# Aws
AWS_CONN_ID: Final[str] = "aws"
AWS_ACCESS_KEY_ID: Final[str] = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY: Final[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION: Final[str] = os.getenv("AWS_REGION")

S3_BUCKET_NAME: Final[str] = os.getenv("S3_BUCKET_NAME")

REDSHIFT_CONN_ID: Final[str] = "redshift"
REDSHIFT_HOST: Final[str] = os.getenv("REDSHIFT_HOST")
REDSHIFT_PORT: Final[str] = os.getenv("REDSHIFT_PORT")
REDSHIFT_DATABASE: Final[str] = os.getenv("REDSHIFT_DATABASE")
REDSHIFT_CLUSTER: Final[str] = os.getenv("REDSHIFT_CLUSTER")
REDSHIFT_MASTER_USERNAME: Final[str] = os.getenv("REDSHIFT_MASTER_USERNAME")
REDSHIFT_MASTER_PASSWORD: Final[str] = os.getenv("REDSHIFT_MASTER_PASSWORD")
