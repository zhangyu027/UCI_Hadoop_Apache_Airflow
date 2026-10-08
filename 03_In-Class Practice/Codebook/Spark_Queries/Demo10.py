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
logs = sc.textFile("hdfs:///user/kunwu/data/hdfslog/*.out.*")


words = logs.flatMap(lambda x: x.split(' '))
print(words.count())



print(words.collect())



print(words.take(3))



print(words.distinct().top(3))



print(words.distinct().first())




