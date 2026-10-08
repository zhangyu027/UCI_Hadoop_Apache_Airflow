# Airflow Docker Compose Kafka dbt Project

This folder starts Airflow and runs the dbt project stored in the sibling folder `../kafka_dbt_project`.

## Correct folder structure

```text
UCI_Hadoop_Apache_Airflow/
├── airflow_docker_compose_kafka_dbt/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── README.md
│   ├── .dbt/
│   │   └── profiles.yml
│   ├── dags/
│   │   └── kafka_dbt_pipeline_dag.py
│   ├── logs/
│   └── plugins/
│
└── kafka_dbt_project/
    ├── dbt_project.yml
    ├── .dbt/profiles.yml
    ├── models/
    └── ...
```

Important: do not keep an empty `kafka_dbt_project` folder inside `airflow_docker_compose_kafka_dbt`.

## Why the Docker volume uses `../kafka_dbt_project`

Docker commands are run from:

```bash
cd ~/projects/UCI_Hadoop_Apache_Airflow/airflow_docker_compose_kafka_dbt
```

The dbt project is one folder above, so the volume mapping is:

```yaml
- ../kafka_dbt_project:/opt/airflow/kafka_dbt_project
```

Inside the Airflow container, dbt sees the project at:

```text
/opt/airflow/kafka_dbt_project
```

## Start Airflow

```bash
cd ~/projects/UCI_Hadoop_Apache_Airflow/airflow_docker_compose_kafka_dbt
echo "AIRFLOW_UID=$(id -u)" > .env
docker compose build --no-cache
docker compose up -d
```

## Check containers

```bash
docker compose ps
```

Expected:

```text
airflow-postgres     healthy
airflow-webserver    Up, port 8081->8080
airflow-scheduler    Up
```

## Initialize the Airflow administrator (first run only)

The `airflow-init` service runs `airflow db migrate` to prepare the metadata database.
It does **not** create a web UI user. After `docker compose up -d`, create an administrator:

```bash
docker compose exec airflow-webserver \
  airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin
```

You should see `User "admin" created with role "Admin"`.

If the user already exists, inspect users and optionally reset the password:

```bash
docker compose exec airflow-webserver airflow users list
docker compose exec airflow-webserver airflow users reset-password --username admin --password admin
```

The `admin` / `admin` credentials are **for local development only**. Use a unique strong password and avoid committing real credentials to Git.

A Flask-Limiter warning about in-memory rate-limit storage may appear in local development; it does not prevent user creation.

## Open Airflow

```text
http://localhost:8081
```

For the first-run administrator setup, see **Initialize the Airflow administrator** above.

## Start the analytics database and Kafka stack

The Airflow metadata database and the analytics database are **different PostgreSQL services**:

- Airflow metadata: host `localhost:5432` (container service `airflow-postgres:5432`)
- Kafka/dbt analytics: host `localhost:5433` (inside its own container: port 5432)

Before running the dbt DAG, start the sibling analytics stack:

```bash
cd ../kafka_dbt_project
docker compose up -d
docker compose ps
cd ../airflow_docker_compose_kafka_dbt
```

The Airflow Compose file passes `DBT_HOST=host.docker.internal` and `DBT_PORT=5433` into its webserver and scheduler. The mounted dbt profile uses these variables. This setup is designed for Docker Desktop on macOS.

**Prepare input data first:** run `consumer2.py` and `producer.py` from separate host terminals in `kafka_dbt_project` (with that project's Python requirements installed). The consumer runs continuously until stopped. The Airflow DAG handles `dbt debug → dbt run → dbt test`; it does not start the Kafka producer or consumer.

## Test dbt inside the Airflow container

```bash
docker exec -it airflow_docker_compose_kafka_dbt-airflow-webserver-1 bash
cd /opt/airflow/kafka_dbt_project
dbt debug --profiles-dir .dbt
dbt run --profiles-dir .dbt
dbt test --profiles-dir .dbt
```

## Verify DAG registration

```bash
docker compose exec airflow-scheduler airflow dags list
```

Only `airflow_docker_compose_kafka_dbt/dags/kafka_dbt_pipeline_dag.py` is the supported DAG definition. The old host-specific duplicate DAG was removed from the sibling project's `dags/` folder.

## Trigger the DAG

In Airflow, search for:

```text
kafka_dbt_pipeline
```

Then click the trigger button.

## Stop Airflow

```bash
docker compose down
```
