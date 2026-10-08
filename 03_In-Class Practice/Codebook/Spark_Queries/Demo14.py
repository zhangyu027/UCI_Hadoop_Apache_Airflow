# Creating RDDs from a Text File or Files

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import count
from pyspark import SparkContext

sc = SparkContext()

##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# sc.textFile(name, minPartitions=None, use_unicode=True)
##### ##### ##### ##### ##### ##### ##### ##### ##### #####
odds = sc.parallelize([1,3,5,7,9])
fibonacci = sc.parallelize([0,1,2,3,5,8])
print(odds.union(fibonacci).collect())
# returns [1, 3, 5, 7, 9, 0, 1, 2, 3, 5, 8]



odds = sc.parallelize([1,3,5,7,9])
fibonacci = sc.parallelize([0,1,2,3,5,8])
print(odds.intersection(fibonacci).collect())
# returns [1, 3, 5]



odds = sc.parallelize([1,3,5,7,9])
fibonacci = sc.parallelize([0,1,2,3,5,8])
print(odds.subtract(fibonacci).collect())
# returns [7, 9]



cities1 = sc.parallelize(
[
   ('Hayward',(37.668819,-122.080795)),
   ('Baumholder',(49.6489,7.3975)),
   ('Alexandria',(38.820450,-77.050552)),
   ('Melbourne', (37.663712,144.844788))
])
cities2 = sc.parallelize(
[
   ('Boulder Creek',(64.0708333,-148.2236111)),
   ('Hayward',(37.668819,-122.080795)),
   ('Alexandria',(38.820450,-77.050552)),
   ('Arlington', (38.878337,-77.100703))
])
print(cities1.subtractByKey(cities2).collect())
# returns:
# [('Baumholder', (49.6489, 7.3975)), ('Melbourne', (37.663712,144.844788))]

print(cities2.subtractByKey(cities1).collect())
# returns:
# [('Boulder Creek', (64.0708333, -148.2236111)),
# ('Arlington', (38.878337, -77.100703))]




