# Day 4 — Apache Airflow Fundamentals Lab

## Goal

This lab teaches core Apache Airflow orchestration concepts with a simple daily ETL pipeline.

## Topics

- DAGs
- Scheduling
- Retries
- PythonOperator
- Task dependencies
- Manual DAG triggering
- Logs and task status
- Execution flow

## Folder structure

```text
day4_airflow_fundamentals_lab/
├── docker-compose.yml
├── README.md
├── dags/
│   └── daily_pipeline_dag.py
├── logs/
└── plugins/
```

## Start Airflow

Run commands from this folder:

```bash
cd ~/UCI_Hadoop_Apache_Airflow/day4_airflow_fundamentals_lab
docker compose up -d
```

## Check containers

```bash
docker compose ps
```

Expected services:

```text
day4-airflow-postgres     healthy
day4-airflow-webserver    Up, port 8083->8080
day4-airflow-scheduler    Up
```

## Open Airflow

```text
http://localhost:8083
```

Login:

```text
Username: admin
Password: admin
```

## DAG

The DAG file is:

```text
dags/daily_pipeline_dag.py
```

Task flow:

```text
extract_data
    ↓
transform_data
    ↓
load_data
```

## Trigger the DAG

1. Open Airflow.
2. Search for `daily_pipeline_dag`.
3. Turn the DAG on.
4. Click the DAG name.
5. Click the trigger button.
6. Open Graph view.
7. Confirm all tasks turn green.

## View logs

Click each task and open logs to see:

```text
Extract step started
Transform step started
Load step started
```

## Stop Airflow

```bash
docker compose down
```

## Full reset

Use this only if you want to delete the Airflow metadata database and start fresh:

```bash
docker compose down -v
docker compose up -d
```
