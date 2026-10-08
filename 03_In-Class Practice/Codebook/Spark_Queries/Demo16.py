# Creating RDDs from a Text File or Files
# -*- coding: utf-8 -*-

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import count
from pyspark.sql.types import StructType,StructField, StringType, IntegerType
from pyspark.sql.types import ArrayType, DoubleType, BooleanType
from pyspark import SparkContext

sc = SparkContext()
spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()

##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# sc.textFile(name, minPartitions=None, use_unicode=True)
##### ##### ##### ##### ##### ##### ##### ##### ##### #####
myrdd = sc.parallelize([('Jeff', 48),('Kellie', 45)])
df = spark.createDataFrame(myrdd)
print(df.collect())
# returns:
# [Row(_1=u'Jeff', _2=48), Row(_1=u'Kellie', _2=45)]






people_json_file = 'file:///home/kunwu/data/sampledata/people.json'
people_df = spark.read.json(people_json_file)
people_df.show()
# returns:
# +----+-------+
# | age| name|
# +----+-------+
# |null|Michael|
# | 30| Andy|
# | 19| Justin|
# +----+-------+





# read an individual file
df = spark.read.text('file:///home/kunwu/python/LearningSpark/data/bike-share/stations/stations.csv')
print(df.take(1))
# returns:
# [Row(value=u'9,Japantown,37.348742,−121.894715,15,San Jose,8/5/2013')]
# you can also read all files from a directory...
df = spark.read.text('file:///home/kunwu/python/LearningSpark/data/bike-share/stations/')
print(df.count())
# returns: 83
df.show()





schema = StructType() \
      .add("station_id",IntegerType(),True) \
      .add("name",StringType(),True) \
      .add("lat",DoubleType(),True) \
      .add("long",DoubleType(),True) \
      .add("dockcount",IntegerType(),True) \
      .add("landmark",StringType(),True) \
      .add("installation",StringType(),True)
f = 'file:///home/kunwu/python/LearningSpark/data/bike-share/stations/stations.csv'
df_with_schema = spark.read.format("csv") \
      .option("header", True) \
      .schema(schema) \
      .load(f)
df_with_schema.printSchema()


parquet_path = "hdfs:///user/kunwu/data/parquet/stations.parquet"
#df_with_schema.write.format("parquet").save(parquet_path)

df = spark.read.parquet(parquet_path)
df.printSchema()
print(df.count())


tripsSchema = StructType() \
   .add("TripID", "integer") \
   .add("Duration", "integer") \
   .add("StartDate", "string") \
   .add("StartStation", "string") \
   .add("StartTerminal", "integer") \
   .add("EndDate", "string") \
   .add("EndStation", "string") \
   .add("EndTerminal", "integer") \
   .add("BikeNo", "integer") \
   .add("SubscriberType", "string") \
   .add("ZipCode", "string")
f = 'file:///home/kunwu/python/LearningSpark/data/bike-share/trips/trips.csv'
df_with_schema = spark.read.format("csv") \
      .option("header", True) \
      .schema(tripsSchema) \
      .load(f)
df_with_schema.printSchema()
parquet_path = "hdfs:///user/kunwu/data/parquet/trips.parquet"
df_with_schema.write.format("parquet").save(parquet_path)



stationsdf = spark.read.parquet(parquet_path)
stationsrdd = stationsdf.rdd
print(stationsrdd)
# returns:
# MapPartitionsRDD[4] at javaToPython at ...

print(stationsrdd.take(1))
# returns:
# [Row(station_id=2, name=u'San Jose Diridon Caltrain Station',lat=37.329732 ...)]



