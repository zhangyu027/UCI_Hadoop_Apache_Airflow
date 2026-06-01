# Day 5–6 Spark + Airflow + PostgreSQL ETL Project

This project supports Day 5–6 Spark + Airflow ETL.

## Start

```bash
cd day5_day6_spark_airflow_etl_project
docker compose down -v
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
