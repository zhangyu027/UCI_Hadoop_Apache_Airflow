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
numbers = sc.range(0, 100000000, 1, 2)
evens = numbers.filter(lambda x: x % 2)

evens.persist()
# instructs Spark to persist evens RDD when the next action requires it

noelements = evens.count()
print(noelements)
# processes evens RDD

print("There are %s elements in the collection" % (noelements))
# returns "There are 500000 elements in the collection"

listofelements = evens.collect()
# REPROCESSES evens RDD
# does NOT have to recompute the evens RDD

print("The first five elements include " + (str(listofelements[0:5])))
# returns "The first five elements include [1, 3, 5, 7, 9]"
