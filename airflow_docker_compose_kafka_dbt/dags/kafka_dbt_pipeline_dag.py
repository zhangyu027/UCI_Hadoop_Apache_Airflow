"""Single Docker-compatible DAG definition for the Kafka/dbt demonstration.

Kafka producer and consumer run separately on the host so localhost:9092 remains
valid; this DAG transforms and tests data already ingested into PostgreSQL.
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

DBT_PROJECT_DIR = "/opt/airflow/kafka_dbt_project"
DBT_PROFILES_DIR = f"{DBT_PROJECT_DIR}/.dbt"

with DAG(
    dag_id="kafka_dbt_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["kafka", "dbt", "data-engineering"],
) as dag:
    dbt_debug = BashOperator(
        task_id="dbt_debug",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt debug --profiles-dir {DBT_PROFILES_DIR}",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt run --profiles-dir {DBT_PROFILES_DIR}",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt test --profiles-dir {DBT_PROFILES_DIR}",
    )

    dbt_debug >> dbt_run >> dbt_test
