# Day 5–6 Spark + Airflow + PostgreSQL ETL Project

This project supports Day 5–6 Spark + Airflow ETL.

## Start

```bash
cd day5_day6_spark_airflow_etl_project
docker compose up --build -d
docker compose ps
```

Open:
```text
http://127.0.0.1:8082
```

Login:

```text
admin / admin
```

Trigger:

```text
day6_api_spark_postgres_etl
```

Expected task flow:

```text
check_services
   ↓
run_spark_etl
   ↓
verify_warehouse_tables
```

## Local ports and troubleshooting

The mock API is available on the Mac at `http://127.0.0.1:8001/sales_events.json`.
The container continues listening on port `8000`, so Airflow uses
`http://mock-api:8000/sales_events.json` (Docker-internal networking).
The Airflow web UI remains at `http://127.0.0.1:8082`.

If Docker reports that host port `8000` is already allocated, this configuration
avoids the conflict without stopping other projects.

Check startup status and logs:

```bash
docker compose ps
docker compose logs --tail=100 mock-api airflow-init airflow-webserver airflow-scheduler
```

The Compose volumes store PostgreSQL data. Avoid `docker compose down -v`
unless you deliberately want to delete those databases.

## Verify outputs

```bash
docker exec -it day56-warehouse-postgres psql -U postgres -d warehouse
```

```sql
select * from public.cleaned_sales_events order by event_date, order_id;
select * from public.daily_sales_summary order by event_date, event;
\q
```

## Debug logs

```bash
docker logs day56-airflow-scheduler --tail 100
docker logs day56-airflow-webserver --tail 100
```
