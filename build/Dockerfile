FROM apache/airflow:2.9.0-python3.10
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         openjdk-17-jre-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

USER airflow

COPY requirements.txt requirements.txt
RUN pip install --upgrade --no-cache-dir -r requirements.txt \
  && rm -f requirements.txt
