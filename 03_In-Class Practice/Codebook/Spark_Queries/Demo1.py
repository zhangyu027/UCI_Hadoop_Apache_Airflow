# Sample PySpark Program to Search for Errors in Log Files

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import count
from pyspark import SparkContext

sc =SparkContext()

# load log files from local filesystem
# loading data into an RDD
logfilesrdd = sc.textFile("file:///var/log/hadoop/hdfs/hadoop-hdfs-*")

# filter log records for errors only
# creating a new RDD using a filter transformation
onlyerrorsrdd = logfilesrdd.filter(lambda line: "ERROR" in line)

# save onlyerrorsrdd as a file
# using an action to save the resultant RDD to disk
onlyerrorsrdd.saveAsTextFile("file:///home/eddeyuzhang/onlyerrorsrdd")


