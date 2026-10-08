# Creating RDDs from a Text File or Files

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import count
from pyspark import SparkContext

sc = SparkContext()

##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# sc.textFile(name, minPartitions=None, use_unicode=True)
##### ##### ##### ##### ##### ##### ##### ##### ##### #####

numbers = sc.parallelize([1,2,3,4,5,6,7,8,9])
print(numbers.reduce(lambda x, y: x + y))


print(numbers.fold(0, lambda x, y: x + y))

numbers = sc.parallelize([1,2,3,4,5,6,7,8,9], 1)
print(numbers.fold(10, lambda x, y: x + y))

numbers = sc.parallelize([1,2,3,4,5,6,7,8,9], 2)
print(numbers.fold(10, lambda x, y: x + y))

numbers = sc.parallelize([1,2,3,4,5,6,7,8,9], 3)
print(numbers.fold(10, lambda x, y: x + y))

numbers = sc.parallelize([1,2,3,4,5,6,7,8,9], 4)
print(numbers.fold(10, lambda x, y: x + y))


def printfunc(x):
   print(x)

logs = sc.textFile("hdfs:///user/kunwu/data/hdfslog/*.out.*")
longwords = logs.flatMap(lambda x: x.split(' ')) \
                .filter(lambda x: len(x) > 12 and len(x) < 50)
  
longwords.foreach(lambda x: printfunc(x))

