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

spark.sql("""
DROP TABLE managed_us_delay_flights_tbl
"""
)

spark.sql("""
CREATE TABLE managed_us_delay_flights_tbl
(
   date STRING, 
   delay INT,
   distance INT, 
   origin STRING, 
   destination STRING
)""")


print("find all flights whose distance is greater than 1,000 miles: ")

spark.sql("""SELECT distance, origin, destination
FROM managed_us_delay_flights_tbl WHERE distance > 1000
ORDER BY distance DESC""").show(10)

print("\n***** ***** ***** ***** \n")


flights_df = (spark.read.format("csv")
   .option("inferSchema", "true")
   .option("header", "true")
   .load(csv_file))
#flights_df.write.saveAsTable("managed_us_delay_flights_tbl2")

print("find all flights whose distance is greater than 1,000 miles: again... ...")

#spark.sql("""SELECT distance, origin, destination
#FROM managed_us_delay_flights_tbl2 WHERE distance > 1000
#ORDER BY distance DESC""").show(10)

print("\n***** ***** ***** ***** \n")
print("\n***** ***** ***** ***** \n")
print("\n***** ***** ***** ***** \n")
print("Creating an unmanaged table")


spark.sql("""
DROP TABLE us_delay_flights_tbl
"""
)


spark.sql("""
CREATE TABLE us_delay_flights_tbl(
   date STRING, 
   delay INT,
   distance INT, 
   origin STRING, 
   destination STRING)
USING csv OPTIONS 
(PATH 'databricks-datasets/learning-spark-v2/flights/departuredelays_noheader.csv')
""")
print("find all flights whose distance is greater than 1,000 miles: ")

spark.sql("""
SELECT distance, origin, destination
FROM us_delay_flights_tbl WHERE distance > 1000
ORDER BY distance DESC""").show(10)





