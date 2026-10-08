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
csv_file = "databricks-datasets/learning-spark-v2/flights/departuredelays.csv"

df_sfo = spark.sql("""
SELECT date, delay, origin, destination FROM
us_delay_flights_tbl WHERE origin = 'SFO'"""
)

df_jfk = spark.sql("""
SELECT date, delay, origin, destination FROM
us_delay_flights_tbl WHERE origin = 'JFK'""")

#since 2.2
#df_sfo.createOrReplaceGlobalTempView("us_origin_airport_SFO_global_tmp_view")
df_jfk.createOrReplaceTempView("us_origin_airport_JFK_tmp_view")

spark.sql("""
SELECT * FROM us_origin_airport_JFK_tmp_view
""").show(2)

