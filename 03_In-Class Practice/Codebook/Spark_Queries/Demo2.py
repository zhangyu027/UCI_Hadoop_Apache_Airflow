# Creating RDDs from a Text File or Files

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import count
from pyspark import SparkContext

sc = SparkContext()

##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# sc.textFile(name, minPartitions=None, use_unicode=True)
##### ##### ##### ##### ##### ##### ##### ##### ##### #####

# load the contents of the entire directory
logs = sc.textFile("hdfs:///user/kunwu/data/hdfslog/")
print(type(logs))
print(logs)
print(logs.take(1))
print(logs.count())
print(logs.getNumPartitions())



# load an individual file
logs = sc.textFile("hdfs:///user/kunwu/data/hdfslog/hadoop-hdfs-namenode-m1.mt.dataapplab.com.log.1")


# load a file or files using a glob pattern
logs = sc.textFile("hdfs:///user/kunwu/data/hdfslog/hadoop-hdfs-namenode*")


##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# sc.wholeTextFiles(path, minPartitions=None, use_unicode=True)
##### ##### ##### ##### ##### ##### ##### ##### ##### #####

logs = sc.wholeTextFiles("hdfs:///user/kunwu/data/hdfslog/*out*")
print(type(logs))
print(logs)
print(logs.take(1))
print(logs.count())
print(logs.getNumPartitions())

