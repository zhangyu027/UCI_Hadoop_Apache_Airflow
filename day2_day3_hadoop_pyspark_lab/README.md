# Day 2–3 — Hadoop HDFS + PySpark Fundamentals Lab

This lab demonstrates basic Hadoop/HDFS concepts and PySpark DataFrame processing in Docker.

## Final result

After running the PySpark job, you should see an output folder:

```text
data/output/category_sales_summary/
├── _SUCCESS
└── part-00000-....csv
```

The CSV result should look like:

```text
category,total_sales,average_sales
Electronics,2500,833.3333333333334
Furniture,900,300.0
Books,65,32.5
```

This confirms the PySpark job ran successfully.

## Folder structure

```text
day2_day3_hadoop_pyspark_lab/
├── Dockerfile.pyspark
├── docker-compose.yml
├── README.md
├── data/
│   └── sales.csv
├── hdfs_examples/
│   └── README.md
└── spark_jobs/
    ├── sales_summary.py
    └── word_count.py
```

## 1. Start Docker Desktop

Make sure Docker Desktop is open and running.

## 2. Go to the project folder

```bash
cd ~/projects/UCI_Hadoop_Apache_Airflow/day2_day3_hadoop_pyspark_lab
```

## 3. Clean old containers

```bash
docker compose down --remove-orphans
docker rm -f day3-pyspark day2-hadoop 2>/dev/null || true
```

## 4. Build and start containers

```bash
docker compose build --no-cache
docker compose up -d
```

## 5. Check containers

```bash
docker compose ps
```

Expected:

```text
day2-hadoop    Up
day3-pyspark   Up
```

## 6. Open Jupyter UI

Open:

```text
http://localhost:8888
```

Token:

```text
admin
```

You can also open directly:

```text
http://localhost:8888/?token=admin
```

## 7. Test PySpark

Run from your Mac terminal:

```bash
docker exec -it day3-pyspark bash
```

Then inside the container:

```bash
python -c "from pyspark.sql import SparkSession; print('PySpark works')"
```

Expected:

```text
PySpark works
```

## 8. Run the sales summary job

Inside the `day3-pyspark` container:

```bash
python /home/jovyan/work/sales_summary.py
```

Expected output includes:

```text
Original Data
Category Sales Summary
Filtered Sales > 100
Window Function Ranking
Wrote category summary to: /home/jovyan/data/output/category_sales_summary
```

## 9. Run the word count job

Inside the `day3-pyspark` container:

```bash
python /home/jovyan/work/word_count.py
```

Expected output includes:

```text
Word Count Results
```

## 10. Verify output in Jupyter

In Jupyter, open:

```text
data/output/category_sales_summary/
```

Open the `part-00000-....csv` file.

Expected rows:

```text
Electronics,2500,833.3333333333334
Furniture,900,300.0
Books,65,32.5
```

Exit:

```bash
exit
```

## 11. Hadoop/HDFS practice

Enter the Hadoop container:

```bash
docker exec -it day2-hadoop bash
```

Check Hadoop:

```bash
hadoop version
hdfs version
```

Check mounted data:

```bash
ls -la /data
cat /data/sales.csv
```

Optional HDFS-style practice:

```bash
hdfs dfs -mkdir -p /data
hdfs dfs -put /data/sales.csv /data/sales.csv
hdfs dfs -ls /data
hdfs dfs -cat /data/sales.csv
```

Exit:

```bash
exit
```

## 12. Stop containers

```bash
docker compose down
```

## 13. Full reset

Use this only if you want to remove outputs and restart fresh:

```bash
docker compose down --remove-orphans
docker rm -f day3-pyspark day2-hadoop 2>/dev/null || true
rm -rf data/output
docker compose build --no-cache
docker compose up -d
```

## Troubleshooting

### Problem: container name already in use

Run:

```bash
docker rm -f day3-pyspark day2-hadoop
docker compose up -d
```

### Problem: `ModuleNotFoundError: No module named 'pyspark'`

Rebuild with the custom Dockerfile:

```bash
docker compose down --remove-orphans
docker compose build --no-cache
docker compose up -d
```

### Problem: Jupyter asks for token

Use:

```text
admin
```

or run:

```bash
docker exec -it day3-pyspark jupyter server list
```

## What this lab demonstrates

- Docker Compose basics
- Hadoop container setup
- HDFS command practice
- Jupyter + PySpark environment
- PySpark DataFrame loading
- Aggregation
- Filtering
- Window functions
- Writing CSV output
