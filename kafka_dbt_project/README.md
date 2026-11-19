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
dbt models (planned expansion):
├── sales_summary (implemented event aggregation)
└── sales_summary (currently implemented; profit models are planned, not yet committed)
    ↓
Airflow DAG orchestration
    ↓
Optional Streamlit dashboard
```

## Important relationship with Airflow

The Airflow project mounts this folder with:

```yaml
- ../kafka_dbt_project:/opt/airflow/kafka_dbt_project
```

Inside the Airflow container, dbt runs from:

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
docker compose up -d
docker compose ps
```

## Install Python dependencies locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

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

The consumer inserts Kafka messages into PostgreSQL.

## Run dbt locally on macOS

**Do not use `/opt/airflow/kafka_dbt_project` in a Mac terminal.** That path exists only inside the Airflow container when the sibling folder is mounted. Start from the repository's dbt project directory (not the repository root):

```bash
cd ~/projects/UCI_Hadoop_Apache_Airflow/kafka_dbt_project
ls -la dbt_project.yml .dbt/profiles.yml
docker compose up -d
docker compose ps
```

The local dbt profile connects to PostgreSQL on `localhost:5433`. For container-based Airflow runs, use `DBT_POSTGRES_HOST=host.docker.internal` and `DBT_POSTGRES_PORT=5433` as configured in the Airflow Compose file.

```bash
dbt debug --profiles-dir .dbt
dbt run --profiles-dir .dbt
dbt test --profiles-dir .dbt
```

Expected output:

```text
Completed successfully
```

## Verify dbt output

```bash
docker exec -it kafka_dbt_project-postgres-1 psql -U postgres -d analytics
```

Then:

```sql
-- View sales summary
select * from sales_summary;

\q
```

## Planned: Annual Profit Analysis

The producer includes profit-event generation, but the profit dbt models described below are not currently committed. Do not expect these model views to exist until their SQL files are added:

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

### Planned dbt Models (not yet in GitHub)

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

## Troubleshooting: dbt project/profile not found

If `dbt debug` reports that `dbt_project.yml` or `.dbt/profiles.yml` is missing, run `pwd` and verify you are in `kafka_dbt_project` on the Mac. Use `ls -la .dbt` to see hidden profile files. Do not run the Docker-only `/opt/airflow/...` path directly on macOS.

To run inside the Airflow container instead:

```bash
cd ~/projects/UCI_Hadoop_Apache_Airflow/airflow_docker_compose_kafka_dbt
docker compose exec airflow-webserver bash
cd /opt/airflow/kafka_dbt_project
dbt debug --profiles-dir .dbt
```

If dbt connects but `dbt run` fails with `relation raw_sales does not exist`, create/populate `raw_sales` using the sample SQL above or run the Kafka consumer first. A successful `dbt debug` checks configuration and connectivity, not the existence of source tables.

**Current GitHub state:** only `models/sales_summary.sql` is committed. Profit-model documentation is forward-looking; do not assume the additional profit models or their tests are runnable.
