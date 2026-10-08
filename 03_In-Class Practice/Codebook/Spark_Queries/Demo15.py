# Creating RDDs from a Text File or Files

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import count
from pyspark import SparkContext

sc = SparkContext()

##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# sc.textFile(name, minPartitions=None, use_unicode=True)
##### ##### ##### ##### ##### ##### ##### ##### ##### #####
numbers = sc.parallelize([0,1,1,2,3,5,8,13,21,34])
print(numbers.min())
# returns 0


numbers = sc.parallelize([0,1,1,2,3,5,8,13,21,34])
print(numbers.max())
# returns 34



numbers = sc.parallelize([0,1,1,2,3,5,8,13,21,34])
print(numbers.mean())
# returns 8.8



numbers = sc.parallelize([0,1,1,2,3,5,8,13,21,34])
print(numbers.sum())
# returns 88



numbers = sc.parallelize([0,1,1,2,3,5,8,13,21,34])
numbers.stdev()
# returns 10.467091286503619



numbers = sc.parallelize([0,1,1,2,3,5,8,13,21,34])
print(numbers.variance())
# returns 109.55999999999999



numbers = sc.parallelize([0,1,1,2,3,5,8,13,21,34])
numbers.stats()
# returns (count: 10, mean: 8.8, stdev: 10.4670912865, max: 34.0, min:0.0)
