#airflow_docker_compose_kafka_dbt

Folder structure required:

UCI_Hadoop_Apache_Airflow/
├── airflow_docker_compose_kafka_dbt/
└── kafka_dbt_project/

IMPORTANT:
In kafka_dbt_project/.dbt/profiles.yml use:

host: airflow-postgres

Run:

echo "AIRFLOW_UID=$(id -u)" > .env
docker compose down -v
docker compose build --no-cache
docker compose up -d

Open:
http://localhost:8081