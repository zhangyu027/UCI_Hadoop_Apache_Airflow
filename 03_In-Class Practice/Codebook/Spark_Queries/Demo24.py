import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import count
from pyspark.sql.types import *

# Create a SparkSession
spark = (SparkSession
   .builder
   .appName("SparkSQLExampleApp")
   .getOrCreate())

# Path to data set
print(spark.catalog.listDatabases())
print(spark.catalog.listTables())
#spark.catalog.listColumns("us_delay_flights_tbl")

