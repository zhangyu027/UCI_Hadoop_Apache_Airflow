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

parquet_path = "hdfs:///user/kunwu/data/parquet/stations.parquet"
df = spark.read.parquet(parquet_path)
df.show(2)
newdf = df.select((df.name).alias("Station Name"))
newdf.show(2)




print(df.columns)
# returns:
# ['station_id', 'name', 'lat', 'long', 'dockcount', 'landmark','installation']
newdf = df.drop(df.installation)
print(newdf.columns)
# returns:
# ['station_id', 'name', 'lat', 'long', 'dockcount', 'landmark']




df.filter(df.name == 'St James Park') \
  .select(df.name,df.lat,df.long) \
  .show()





rdd = sc.parallelize([('Jeff', 48),('Kellie', 45),('Jeff', 48)])
df = spark.createDataFrame(rdd)
df.show()
# returns:
# +------+---+
# | _1| _2|
# +------+---+
# | Jeff| 48|
# |Kellie| 45|
# | Jeff| 48|
# +------+---+

df.distinct().show()
# returns:
# +------+---+
# | _1| _2|
# +------+---+
# |Kellie| 45|
# | Jeff| 48|
# +------+---+
