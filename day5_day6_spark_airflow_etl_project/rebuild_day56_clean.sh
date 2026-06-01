#!/usr/bin/env bash
set -euo pipefail

# Run this from the day5_day6_spark_airflow_etl_project folder.
docker compose down --volumes --remove-orphans || true

docker rm -f day56-airflow-scheduler day56-airflow-webserver day56-airflow-init 2>/dev/null || true

docker rmi -f day56-airflow-spark-java-fixed:latest 2>/dev/null || true

docker compose build --no-cache --pull airflow-init airflow-webserver airflow-scheduler

docker compose up -d

echo "\nChecking Java inside scheduler..."
docker exec -it day56-airflow-scheduler bash -lc 'java -version && echo JAVA_HOME=$JAVA_HOME && which java && ps --version | head -1'
