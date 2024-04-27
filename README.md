<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD041 -->

<div align="center">
  <h2 align="center">🚖 ETL Platform: Analyzing NYC Yellow Taxi Trips with Airflow, FastAPI, and Cloud Integration</h2>
  <p align="center">
    <i>The aim of project</i> is to create modern end-to-end ETL platform for Big Data analysis ❤️! <br>
    A hands-on experience with the latest library versions in a fully dockerized environment
    for <br> NYC Yellow Taxi Trips Analytics.<br>
    With Airflow and PySpark at its core, you'll explore the power of large-scale data processing using DAGs.<br>
    Choose between GCP or AWS for cloud solutions and manage your infrastructure with Terraform.<br>
    Enjoy playing with FastAPI web application for easy access to trip analytics.
  </p>
</div>

#### 🏆 The ETL platform does simple task:

The system fetches trip data from a specified URL,
conducts fundamental daily analytics including passenger count, distance traveled, and maximum trip distance.
Subsequently, it uploads the computed analytics results onto cloud storage provided by the chosen cloud provider.
ETL platform facilitates seamless data transfer from the storage platform to a designated database. <br>
Furthermore, the system offers the functionality to retrieve insights via an accessible API endpoint.

## 🍰 ETL Platform Features

- 💚 ETL platform is open-source and flexible playground for Big Data analysis based on standalone
classic 🚕 [ Yellow Taxi Trip Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).
- 📦 Fully dockerized via [Docker Compose](https://docs.docker.com/compose/) with latest library versions (🐍 Python 3.10+).
- 💪 Harnesses the power of [Airflow](https://airflow.apache.org/) and [PySpark](https://spark.apache.org/docs/latest/api/python/index.html) for efficient processing of large datasets.
- 🔍 Offers [Google Cloud Platform](https://cloud.google.com/?hl=en) (Google Cloud Storage, BigQuery), [Amazon Web Services](https://aws.amazon.com/) (S3, Redshift) cloud solutions, based on user preference.
- ☁️ Cloud infrastructure management handled through [Terraform](https://www.terraform.io/).
- 🌟 Includes a user-friendly [FastApi](https://fastapi.tiangolo.com/) web application with [Traefik](https://traefik.io/) enabling easy access to trip analytics.
- 🔧 Uses [Poetry](https://python-poetry.org/) for dependencies management.
- 📄 Provides basic [Pre-commit](https://pre-commit.com/) hooks, [Ruff](https://docs.astral.sh/ruff/) formatting, and [Checkov](https://www.checkov.io/) for security and compliance issues.

## 🚀 Getting Started

### 🎌 Installation

1. Clone the ETL platform project.
2. Check existence or install:
- [Docker and Docker Compose](https://docs.docker.com/engine/install/).
- [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) to manage cloud infrastructure.
3. Get and place credentials for clouds (AWS, GCP or both):
- Google Cloud Platform:
    - [Create project](https://developers.google.com/workspace/guides/create-project).
    - [Create service Account](https://cloud.google.com/iam/docs/keys-create-delete).
    - [Add roles and policies](https://cloud.google.com/iam/docs/service-account-permissions) for Google Cloud Storage (for ex. BigQueryAdmin)
and BigQuery (StorageAdmin).
    - Download .json file with credentials and place it under `credentials/gcp` folder.
- Amazon Web Services:
  - [Add roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html) for selected user.
  - [Create `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) in specified `AWS_REGION`
(default for ETL platform is `us-east-1`) and store in safe place.
4. Apply Cloud infrastructure via Terraform from root folder:
```bash
cd terraform/<cloud-provider>
terraform init
terraform plan
terraform apply -auto-approve
```
❗ For `Aws` cloud provider you have to pass
`aws_access_key_id`, `aws_secret_access_key`, `redshift_master_password`. <br>
As an output you will get `redshift_cluster_endpoint` where `redshift-host`
could be extracted and passed in `.env` file below.
❗ For `Gcp` cloud provider you have to pass
`credentials_path=../../credentials/gcp/<filename>.json`, `project_name`.

🌞 If previous steps done successfully, you will see `Apply complete!` message from Terraform
and Cloud Infrastructure is ready to use!

5. Update `.env` file under `build` folder with actual credentials:
```dotenv
# Gcp
GCP_CREDENTIALS_PATH=/opt/airflow/credentials/gcp/<filename>.json
GCP_PROJECT_NAME=<project-name>

# Aws
AWS_ACCESS_KEY_ID=<access-key-id>
AWS_SECRET_ACCESS_KEY=<secret-access-key-id>

REDSHIFT_HOST=<redshift-host>
REDSHIFT_MASTER_PASSWORD=<redshift-master-password>
```
⚠️ Replace default values (such as passwords) in `.env` file.

6. Up project via docker-compose in `build` folder:
```bash
docker-compose up --build
```
7. Check if build is done successfully 🎉 (provide `_AIRFLOW_WWW_USER_USERNAME`
`_AIRFLOW_WWW_USER_PASSWORD` from `.env` to authenticate): ```http://localhost:8080```.

## 💡 Usage

1. In your environment will be a DAG (called `ETL_trip_data`)
which you can trigger with default parameters (and selected Cloud Provider):
![DAG](https://github.com/vladyslavyaloveha/etl_platform/blob/master/.screenshots/dag.png?raw=true)

2. Dag Graph you can find under `http://localhost:8080/dags/ETL_trip_data/grid?tab=graph`:
![Graph](https://github.com/vladyslavyaloveha/etl_platform/blob/master/.screenshots/graph.png?raw=true)

3. FastApi web application docs you can find under `http://localhost:8009/docs`.
4. Spark interface: `http://localhost:8082`.
5. Traefik monitoring: `http://localhost:8085`.

## 💻 Tech Stack

![Python](https://img.shields.io/badge/Python-3106AB?style=flat&logo=python&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Airflow-00AD46?logo=apache-airflow&style=flat)
![PySpark](https://img.shields.io/badge/PySpark-005B81?logo=apache-spark&style=flat)
![Docker](https://img.shields.io/badge/Docker-blue?logo=docker&style=flat)
![AWS](https://img.shields.io/badge/AWS-494949?logo=amazon-aws&style=flat)
![S3](https://img.shields.io/badge/S3%20Bucket-orange?logo=amazon-s3&style=flat&logoColor=white)
![Redshift](https://img.shields.io/badge/Redshift-red?logo=amazon-redshift&style=flat&logoColor=white)
![GCP](https://img.shields.io/badge/Google_Cloud-4285F4?style=flat&logo=google-cloud&logoColor=white)
![Google Cloud Storage](https://img.shields.io/badge/Google_Cloud_Storage-494949?style=flat&logo=google-cloud&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-494949?logo=google-cloud&style=flat&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-blueviolet?logo=terraform&style=flat&logoColor=white)
![FastApi](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&style=flat)
![Traefik](https://img.shields.io/badge/Traefik-blue?logo=traefik&style=flat&logoColor=white)
![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)
![pre-commit](https://img.shields.io/badge/pre--commit-494949?logo=pre-commit&style=flat&logoColor=white)
![checkov](https://img.shields.io/badge/Checkov-052882?style=flat&logoColor=white)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json&logoColor=white&style=flat)
![.parquet](https://img.shields.io/badge/.parquet-494949?style=flat&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=fff&style=flat)
![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=fff&style=flat)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?logo=githubactions&logoColor=fff&style=flat)
![Markdown](https://img.shields.io/badge/Markdown-000?logo=markdown&logoColor=fff&style=flat)
![License](https://img.shields.io/badge/license-MIT-3178C6?style=flat)

## 😀 Enjoying this project? Support via github star ⭐

## ✨ Adjust & Improve project for your needs

## 📈 Metrics

![Alt](https://repobeats.axiom.co/api/embed/f641429d3888204d956662b40877853b1b29c5ce.svg "Repobeats")
