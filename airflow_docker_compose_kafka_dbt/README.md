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

Login:

```text
Username: admin
Password: admin
```

## Test dbt inside the Airflow container

```bash
docker exec -it airflow_docker_compose_kafka_dbt-airflow-webserver-1 bash
cd /opt/airflow/kafka_dbt_project
dbt debug --profiles-dir .dbt
dbt run --profiles-dir .dbt
dbt test --profiles-dir .dbt
```

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
