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
cd ~/UCI_Hadoop_Apache_Airflow/day2_day3_hadoop_pyspark_lab
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

From your **Mac terminal**, run this command after Docker is started (no need to enter the container first):

```bash
docker exec -it day3-pyspark python /home/jovyan/work/sales_summary.py
```

If you are already inside the `day3-pyspark` container from Step 7, use `python /home/jovyan/work/sales_summary.py` instead.

Expected output includes:

```text
Original Data
Category Sales Summary
Filtered Sales > 100
Window Function Ranking
Wrote category summary to: /home/jovyan/data/output/category_sales_summary
```

### Verify generated CSV files

From your **Mac terminal**, run:

```bash
docker exec day3-pyspark ls -la /home/jovyan/data/output/category_sales_summary/
```

Expected files include `_SUCCESS` and `part-00000-<generated-id>-c000.csv` (the unique filename changes on each run). To see the CSV contents:

```bash
docker exec day3-pyspark sh -c 'cat /home/jovyan/data/output/category_sales_summary/part-*.csv'
```

Docker Compose maps the local `./data` directory to `/home/jovyan/data` inside the PySpark container. Therefore the CSV also appears at `data/output/category_sales_summary/` in the project on your Mac. Starting Docker or opening JupyterLab alone does **not** generate output; run the script each time you need to regenerate it. Spark uses overwrite mode, so rerunning the job replaces the previous output directory.

## 9. Run the word count job

From your Mac terminal:

```bash
docker exec -it day3-pyspark python /home/jovyan/work/word_count.py
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

Refresh the JupyterLab file browser if needed, then open the generated `part-00000-....csv` file.

Expected rows:

```text
Electronics,2500,833.3333333333334
Furniture,900,300.0
Books,65,32.5
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

### Problem: `output/part-00000` or `category_sales_summary` is missing

The job creates the output only after successful execution. From the Mac terminal run:

```bash
docker compose ps
docker exec -it day3-pyspark python /home/jovyan/work/sales_summary.py
docker exec day3-pyspark ls -la /home/jovyan/data/output/category_sales_summary/
```

Check the job's terminal errors if it fails. In JupyterLab, refresh the file browser and open `data/output/category_sales_summary/`. The file is named `part-00000-<generated-id>-c000.csv`, **not** exactly `part-0000`.

### GitHub and generated files

Keep `data/sales.csv`, Python source, Docker configuration, and README in Git. Spark-generated files in `data/output/` can be regenerated and should generally be ignored rather than committed. If output files were previously tracked, removing them from the Git index once with `git rm -r --cached --ignore-unmatch day2_day3_hadoop_pyspark_lab/data/output/` stops tracking without deleting local files.

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
