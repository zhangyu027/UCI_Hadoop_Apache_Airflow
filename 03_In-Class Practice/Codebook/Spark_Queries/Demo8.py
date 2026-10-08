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


words = logs.flatMap(lambda x: x.split(' '))
print(words.take(5))
# returns [u'2020-11-30', u'09:36:39,824', u'INFO', u'', u'BlockStateChange']

lowercase = words.map(lambda x: x.lower())
print(lowercase.take(5))
# returns [u'2020-11-30', u'09:36:39,824', u'info', u'', u'blockstatechange']

longwords = lowercase.filter(lambda x: len(x) > 12)
print(longwords.take(2))
# returns [u'blockstatechange', u'(blockmanager.java:computereplicationworkforblocks(1588))']

