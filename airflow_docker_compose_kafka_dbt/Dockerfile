FROM apache/airflow:2.9.3-python3.10

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

USER airflow
COPY requirements.txt /requirements.txt

# Match dependencies to the Airflow and Python versions in the base image.
RUN pip install --no-cache-dir \
    "apache-airflow==2.9.3" \
    -r /requirements.txt \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.3/constraints-3.10.txt"
