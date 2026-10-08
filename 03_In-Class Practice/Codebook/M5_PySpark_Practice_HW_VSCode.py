"""
VS Code Runnable PySpark Practice
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, when, col

# Create Spark Session
spark = SparkSession.builder \
    .appName("PySparkPractice") \
    .getOrCreate()

print("Spark session created successfully")

# =========================
# Example Dataset Loading
# =========================

# Replace with your local CSV path
csv_path = "./data/flights.csv"

try:
    df = spark.read.csv(csv_path, header=True, inferSchema=True)

    print("Dataset Loaded")
    df.printSchema()

    # =========================
    # Student Practice 1
    # =========================
    print("\nPractice 1: Show first 5 rows")
    df.show(5)

    # =========================
    # Student Practice 2
    # =========================
    print("\nPractice 2: Count total records")
    print(df.count())

    # =========================
    # Student Practice 3
    # =========================
    print("\nPractice 3: Average Arrival Delay by Origin")

    if "Origin" in df.columns and "ArrDelay" in df.columns:
        df.groupBy("Origin").agg(
            avg("ArrDelay").alias("avg_delay")
        ).show()

    # =========================
    # Student Practice 4
    # =========================
    print("\nPractice 4: Create Delay Flag")

    if "ArrDelay" in df.columns:
        df = df.withColumn(
            "delay_flag",
            when(col("ArrDelay") > 15, "Delayed").otherwise("OnTime")
        )

        df.select("delay_flag").show(5)

except Exception as e:
    print("Error loading dataset:")
    print(e)

finally:
    spark.stop()
    print("Spark session stopped")
