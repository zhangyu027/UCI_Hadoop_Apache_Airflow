# Creating RDDs from JSON

import sys
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import count
from pyspark import SparkContext

sc = SparkContext()

spark = SparkSession.builder \
    .master("local[1]") \
    .appName("SparkByExamples.com") \
    .getOrCreate()

##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# 1. create an RDD by using parallelize()
##### ##### ##### ##### ##### ##### ##### ##### ##### #####
parallelrdd = sc.parallelize([0, 1, 2, 3, 4, 5, 6, 7, 8])
print(parallelrdd)
# notice the type of RDD created:
# ParallelCollectionRDD[0] at parallelize at PythonRDD.scala:423

print(parallelrdd.count())
# this action will return 9 as this is the number of elements in our collection

print(parallelrdd.collect())
# will return the parallel collection as a list as follows:
# [0, 1, 2, 3, 4, 5, 6, 7, 8]


##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# 2. range()
##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# create an RDD with 1000 integers starting at 0 in increments of 1
# across 2 partitions
range_rdd = sc.range(0, 1000, 1, 2)
print(range_rdd)
# note the PythonRDD type, as range is a native Python function
# PythonRDD[1] at RDD at PythonRDD.scala:43

print(range_rdd.getNumPartitions())
# should return 2 as we requested numSlices=2 range_rdd.min()
# should return 0 as this was out start argument

print(range_rdd.max())
# should return 999 as this is 1000 increments of 1 starting from 0

print(range_rdd.take(5))
# should return [0, 1, 2, 3, 4]


##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# 3. create empty RDD
##### ##### ##### ##### ##### ##### ##### ##### ##### #####
emptyRDD  = sc.emptyRDD()
print("is Empty RDD  : " + str(emptyRDD.isEmpty()))
emptyRDD2 = sc.parallelize([])
print("is Empty RDD2 : " + str(emptyRDD2.isEmpty()))


