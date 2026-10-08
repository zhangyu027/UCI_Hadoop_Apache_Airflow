# Creating RDDs from a Text File or Files
# -*- coding: utf-8 -*-

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import count
from pyspark import SparkContext
from pyspark.sql.types import *

sc = SparkContext()
spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()

##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# sc.textFile(name, minPartitions=None, use_unicode=True)
##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# read an individual file

f = 'file:///home/kunwu/python/LearningSpark/data/bike-share/stations/stations.csv'
rdd = sc.textFile(f) \
        .map(lambda x: x.split(',')) \
        .map(lambda x: (int(x[0]), str(x[1]),
                        float(x[2]), float(x[3]),
                        int(x[4]), str(x[5]), str(x[6])))

print(rdd.take(1))
# returns:
# [(2, 'San Jose Diridon Caltrain Station', 37.329732, −121.901782, 27, 'San Jose','8/6/2013')]

df = spark.createDataFrame(rdd)
df.printSchema()
# returns:
# root
# |-- _1: long (nullable = true)
# |-- _2: string (nullable = true)
# |-- _3: double (nullable = true)
# |-- _4: double (nullable = true)
# |-- _5: long (nullable = true)
# |-- _6: string (nullable = true)
# |-- _7: string (nullable = true)




rdd = sc.parallelize( \
   ['{"name":"Adobe on Almaden", "lat":37.331415, "long":−121.8932}',\
    '{"name":"Japantown", "lat":37.348742, "long":−121.894715}'])
df = spark.read.json(rdd)
df.printSchema()
# returns:
# root
# |-- lat: double (nullable = true)
# |-- long: double (nullable = true)
# |-- name: string (nullable = true)




myschema = StructType([ \
   StructField("station_id", IntegerType(), True), \
   StructField("name", StringType(), True), \
   StructField("lat", FloatType(), True), \
   StructField("long", FloatType(), True), \
   StructField("dockcount", IntegerType(), True), \
   StructField("landmark", StringType(), True), \
   StructField("installation", StringType(), True) \
])
rdd = sc.textFile(f) \
        .map(lambda x: x.split(',')) \
        .map(lambda x: (int(x[0]), str(x[1]),
                        float(x[2]), float(x[3]),
                        int(x[4]), str(x[5]), str(x[6])))
df = spark.createDataFrame(rdd, myschema)
df.printSchema()
# returns:
# root
# |-- station_id: integer (nullable = true)
# |-- name: string (nullable = true)
# |-- lat: float (nullable = true)
# |-- long: float (nullable = true)
# |-- dockcount: integer (nullable = true)
# |-- landmark: string (nullable = true)
# |-- installation: string (nullable = true)
