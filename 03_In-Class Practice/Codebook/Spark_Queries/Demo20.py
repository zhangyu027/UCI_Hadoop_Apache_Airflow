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
stations = spark.read.parquet(parquet_path)
stations.show(2)


parquet_path = "hdfs:///user/kunwu/data/parquet/trips.parquet"
trips = spark.read.parquet(parquet_path)
trips.show(2)


joined = trips.join(stations, trips.StartTerminal == stations.station_id)
joined.printSchema()

joined.select(joined.StartStation, joined.Duration) \
      .show(2)




stations.orderBy([stations.name], ascending=False) \
        .select(stations.name) \
        .show(2)
# returns:
# +--------------------+
# | name|
# +--------------------+
# |Yerba Buena Cente...|
# |Washington at Kea...|
# +--------------------+
# only showing top 2 rows




averaged = trips.groupBy([trips.StartTerminal]) \
                .avg('Duration') \
                .show(2)
# returns:
# +-------------+------------------+
# |startterminal| avg(duration)|
# +-------------+------------------+
# | 31|2747.6333021515434|
# | 65| 626.1329988365329|
# +-------------+------------------+
# only showing top 2 rows
