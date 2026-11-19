# Kafka + dbt Modern Data Engineering Project

This folder contains the dbt project and the Kafka/PostgreSQL demo scripts used by the Airflow pipeline in the sibling folder:

```text
../airflow_docker_compose_kafka_dbt
```

## Folder structure

```text
UCI_Hadoop_Apache_Airflow/
├── airflow_docker_compose_kafka_dbt/
└── kafka_dbt_project/
    ├── .dbt/
    │   └── profiles.yml
    ├── models/
    │   ├── sales_summary.sql
    │   └── schema.yml
    ├── producer.py
    ├── consumer.py
    ├── consumer2.py
    ├── dashboard.py
    ├── dbt_project.yml
    ├── docker-compose.yml
    ├── requirements.txt
    └── README.md
```

## What this project demonstrates

### Original Flow
```text
Kafka Producer (sales_topic)
    ↓
Kafka Consumer
    ↓
PostgreSQL raw_sales table
    ↓
dbt sales_summary model
```

### Enhanced Flow (with Annual Profit Data)
```text
Kafka Producer (dual topics)
├── sales_topic → raw_sales table
└── profit_events → raw_profit_events table
    ↓
Multiple dbt models:
├── sales_summary (event aggregation)
├── profit_summary (annual profit by category & year)
├── product_profit_analysis (product-level metrics)
└── yearly_profit_trends (year-over-year comparison)
    ↓
Airflow DAG orchestration
    ↓
Optional Streamlit dashboard
```

## Where to run dbt: Mac vs. Airflow container

**For a Mac terminal (recommended for standalone labs):** use the local project folder, not `/opt/airflow`:

```bash
cd ~/projects/UCI_Hadoop_Apache_Airflow/kafka_dbt_project
source .venv/bin/activate
dbt debug --profiles-dir .dbt
dbt run --profiles-dir .dbt
dbt test --profiles-dir .dbt
```

**For an Airflow container shell only:** `/opt/airflow/kafka_dbt_project` is a path inside the Docker container; it does not exist on your Mac. The commands below require an interactive shell inside a running Airflow container with dbt installed.

The Airflow project mounts this folder with:

```yaml
- ../kafka_dbt_project:/opt/airflow/kafka_dbt_project
```

Once inside the Airflow container shell, dbt runs from:

```bash
cd /opt/airflow/kafka_dbt_project
dbt debug --profiles-dir .dbt
dbt run --profiles-dir .dbt
dbt test --profiles-dir .dbt
```

## Start standalone Kafka and PostgreSQL

Run this only if you want to test Kafka and PostgreSQL from this folder directly:

```bash
cd ~/projects/UCI_Hadoop_Apache_Airflow/kafka_dbt_project
docker compose up -d postgres zookeeper kafka
docker compose ps -a
nc -vz localhost 9092
```

## Install Python dependencies locally

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python --version  # should be Python 3.10.x
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Reliable startup and troubleshooting

1. Start Docker Desktop and verify it is ready with `docker info`.
2. Start all three services with `docker compose up -d postgres zookeeper kafka`.
3. Check `docker compose ps -a`: Kafka, ZooKeeper, and PostgreSQL must all show `Up`.
4. Confirm Kafka is reachable with `nc -vz localhost 9092` before running the consumer.
5. If Kafka shows `Exited (1)`, inspect `docker compose logs --tail=100 kafka` and `docker compose logs --tail=50 zookeeper`. ZooKeeper may need time to become ready; retry `docker compose up -d kafka` after checking logs.
6. `ValueError: Invalid file object: None` during `KafkaConsumer` initialization can occur when the broker is unreachable. Check Kafka status and port 9092 first.
7. `ModuleNotFoundError: No module named 'psycopg2'`: activate `.venv` and install requirements using `python -m pip install -r requirements.txt`.
8. If `psycopg2-binary==2.9.9` fails to build with Python 3.13, recreate `.venv` using Python 3.10; do not use the wrong interpreter to create the virtual environment.
9. If dbt cannot connect to PostgreSQL, check `docker compose ps -a` and confirm localhost port `5433` is published.

For a fresh start, run the consumer in Terminal 1, then the producer in Terminal 2. Run dbt only after records have arrived in PostgreSQL. Use `docker compose down` to stop services; avoid `docker compose down -v` unless you intend to delete persistent PostgreSQL data.

## Create sample PostgreSQL table

```bash
docker exec -it kafka_dbt_project-postgres-1 psql -U postgres -d analytics
```

Then run:

```sql
create table if not exists raw_sales (
    user_id integer,
    event varchar(50),
    amount integer
);

insert into raw_sales (user_id, event, amount)
values
    (1, 'purchase', 100),
    (2, 'purchase', 200),
    (3, 'purchase', 300);

select * from raw_sales;
\q
```

## Run Kafka producer and consumer

Terminal 1:

```bash
python consumer2.py
```

Terminal 2:

```bash
python producer.py
```

The consumer creates `raw_sales` and `raw_profit_events` if they do not exist, then inserts Kafka messages into PostgreSQL. Keep the consumer running while the producer sends events.

Verify counts from another terminal:

```bash
docker compose exec postgres psql -U postgres -d analytics -c "SELECT COUNT(*) FROM raw_sales;"
docker compose exec postgres psql -U postgres -d analytics -c "SELECT COUNT(*) FROM raw_profit_events;"
```


## Run dbt locally

```bash
dbt debug --profiles-dir .dbt
dbt run --profiles-dir .dbt
dbt test --profiles-dir .dbt
```

`dbt debug` should confirm the connection. `dbt run` builds the SQL models actually present in `models/`; inspect the output for errors rather than assuming all documented profit models exist. The current repository contains `sales_summary.sql` but does not yet include the three profit SQL model files described below. Their entries in `schema.yml` do not create models by themselves. Run `dbt test` after resolving missing-model references and test definitions.

## Verify dbt output

```bash
docker exec -it kafka_dbt_project-postgres-1 psql -U postgres -d analytics
```

Then (only query models that `dbt run` actually created):

```sql
-- View sales summary
select * from sales_summary;

-- The following queries require adding the corresponding profit SQL models first.
-- View profit summary (annual profit by category and year)
select * from profit_summary;

-- View product-level profit analysis
select * from product_profit_analysis order by total_profit desc;

-- View year-over-year profit trends
select * from yearly_profit_trends order by year desc, annual_profit desc;

-- View raw profit events
select * from raw_profit_events limit 10;

\q
```

## New Data: Annual Profit Analysis

The producer now generates profit data in addition to sales events:

### Profit Event Fields
- `product_id` - Unique identifier for the product
- `product_name` - Name of the product
- `category` - Product category (Electronics, Clothing, Home, Food)
- `year` - Calendar year (2023, 2024, 2025)
- `quantity` - Units sold in transaction
- `revenue` - Total revenue (price × quantity)
- `cost` - Total cost of goods sold
- `profit` - Net profit (revenue - cost)
- `profit_margin` - Profit margin percentage

### Planned dbt Models (SQL files not yet implemented)

**profit_summary**: Annual aggregates by category and year
- Total transactions and quantity
- Revenue, cost, and profit totals
- Average and overall profit margins

**product_profit_analysis**: Product-level metrics across all time
- Transaction count and total quantities
- Revenue and profit by product
- Min, max, and average profit margins

**yearly_profit_trends**: Year-over-year comparison by category
- Annual revenue, cost, and profit
- Profit margin percentage trends
- Track business growth across years



## Run dashboard

```bash
streamlit run dashboard.py
```

## Stop standalone services

```bash
docker compose down
```

Use the Airflow folder if you want to run the orchestrated DAG:

```bash
cd ../airflow_docker_compose_kafka_dbt
docker compose up -d
```
