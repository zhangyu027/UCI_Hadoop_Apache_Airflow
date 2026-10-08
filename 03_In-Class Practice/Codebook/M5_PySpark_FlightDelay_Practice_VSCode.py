"""
M5 PySpark Flight Delay Practice — VS Code Runnable Script

Use Python 3.11, not Python 3.13.

Setup:
conda create -n pyspark311 python=3.11 -y
conda activate pyspark311
pip install pyspark==3.5.1 pandas

Run:
python M5_PySpark_FlightDelay_Practice_VSCode_FIXED.py
"""

import os
import sys
from pathlib import Path

if sys.version_info >= (3, 13):
    raise RuntimeError(
        "PySpark is not recommended with your current Python 3.13 environment. "
        "Please create and use a Python 3.11 environment."
    )

os.environ["SPARK_LOCAL_DIRS"] = str(Path("./spark_tmp").resolve())
Path("./spark_tmp").mkdir(exist_ok=True)

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, when

spark = (
    SparkSession.builder
    .appName("M5_FlightDelay_VSCode")
    .master("local[*]")
    .config("spark.driver.memory", "2g")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")
print("Spark session created successfully")

csv_path = Path("data/flights.csv")

if not csv_path.exists():
    print("Data file not found:", csv_path.resolve())
    print("Create a data folder and place your flight delay CSV file as data/flights.csv")
else:
    df = spark.read.csv(str(csv_path), header=True, inferSchema=True)
    df.printSchema()
    df.show(5)

    print("\nPractice Answer 1: First 10 rows")
    df.show(10)

    print("\nPractice Answer 2: Total records")
    print(df.count())

    if "Origin" in df.columns and "ArrDelay" in df.columns:
        print("\nPractice Answer 3: Average arrival delay by Origin")
        df.groupBy("Origin").agg(
            avg("ArrDelay").alias("avg_delay")
        ).orderBy(col("avg_delay").desc()).show()

        print("\nPractice Answer 4: Delay flag")
        df = df.withColumn(
            "delay_flag",
            when(col("ArrDelay") > 15, "Delayed").otherwise("OnTime")
        )
        df.select("Origin", "Dest", "ArrDelay", "delay_flag").show(10)
    else:
        print("Expected columns Origin and ArrDelay were not found.")

spark.stop()
print("Spark stopped")