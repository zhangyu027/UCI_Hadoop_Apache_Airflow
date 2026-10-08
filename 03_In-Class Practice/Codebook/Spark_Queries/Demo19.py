# Creating RDDs from a Text File or Files
# -*- coding: utf-8 -*-

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import count
from pyspark import SparkContext
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.types import *

sc = SparkContext()
spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()

##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# sc.textFile(name, minPartitions=None, use_unicode=True)
##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# read an individual file

parquet_path = "hdfs:///user/kunwu/data/parquet/stations.parquet"
df = spark.read.parquet(parquet_path)
df.show(2)


lat2dir = udf(lambda x: 'N' if x > 0 else 'S', StringType())
lon2dir = udf(lambda x: 'E' if x > 0 else 'W', StringType())

df.select(df.lat, lat2dir(df.lat).alias('latdir'),
          df.long, lon2dir(df.lat).alias('longdir')) \
   .show(5)
# returns:
# +---------+------+-----------+-------+
# | lat|latdir| long|longdir|
# +---------+------+-----------+-------+
# |37.329732| N|−121.901782| E|
# |37.330698| N|−121.888979| E|
# |37.333988| N|−121.894902| E|
# |37.331415| N| −121.8932| E|
# |37.336721| N|−121.894074| E|
# +---------+------+-----------+-------+
# only showing top 5 rows
