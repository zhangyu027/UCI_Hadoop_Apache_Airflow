# Creating RDDs from a Text File or Files

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import count
from pyspark import SparkContext

sc = SparkContext()

##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# sc.textFile(name, minPartitions=None, use_unicode=True)
##### ##### ##### ##### ##### ##### ##### ##### ##### #####

stores = sc.parallelize([
   (100, 'Boca Raton'),
   (101, 'Columbia'),
   (102, 'Cambridge'),
   (103, 'Naperville')
])
# stores schema (store_id, store_location)

salespeople = sc.parallelize([
   (1, 'Henry', 100),
   (2, 'Karen', 100),
   (3, 'Paul', 101),
   (4, 'Jimmy', 102),
   (5, 'Janice', None)
])
# salespeople schema (salesperson_id, salesperson_name, store_id)

print(salespeople.keyBy(lambda x: x[2]) \
                 .join(stores).collect())
# returns: 
# [
#  (100, ((1, 'Henry', 100), 'Boca Raton')),
#  (100, ((2, 'Karen', 100), 'Boca Raton')),
#  (102, ((4, 'Jimmy', 102), 'Cambridge')),
#  (101, ((3, 'Paul', 101), 'Columbia'))
# ]


print(salespeople.keyBy(lambda x: x[2]) \
                 .leftOuterJoin(stores) \
                 .filter(lambda x: x[1][1] is None) \
                 .map(lambda x: "salesperson " + x[1][0][1] + " has no store") \
                 .collect())
# returns ['salesperson Janice has no store']



print(salespeople.keyBy(lambda x: x[2]) \
                 .rightOuterJoin(stores) \
                 .filter(lambda x: x[1][0] is None) \
                 .map(lambda x: x[1][1] + " store has no salespeople") \
                 .collect() )
# returns ['Naperville store has no salespeople']



print(salespeople.keyBy(lambda x: x[2]) \
                 .fullOuterJoin(stores) \
                 .filter(lambda x: x[1][0] is None or x[1][1] is None) \
                 .collect() )
# returns [(,([5,'Janice',], None)),(103,(None,[103,'Naperville']))]



print(salespeople.keyBy(lambda x: x[2]) \
                 .cogroup(stores).take(1))
# returns:
# [(None, (<pyspark.resultiterable.ResultIterable object at ...>,
# <pyspark.resultiterable.ResultIterable object at ...>))]

print(salespeople.keyBy(lambda x: x[2]) \
                 .cogroup(stores) \
                 .mapValues(lambda x: [item for sublist in x for item in sublist]) \
                 .collect()
# using the mapValues() to process the Iterable object returns:
# [(None, [(5, 'Janice', None)]),
# (100, [(1, 'Henry', 100), (2, 'Karen', 100), 'Boca Raton']),
# (102, [(4, 'Jimmy', 102), 'Cambridge']), (101, [(3, 'Paul', 101),'Columbia']),
# (103, ['Naperville'])]



print(salespeople.keyBy(lambda x: x[2]) \
                 .cartesian(stores).take(1))
# returns:
# [((100, (1, 'Henry', 100)), (100, 'Boca Raton'))]

print(salespeople.keyBy(lambda x: x[2]) \
                 .cartesian(stores).count())
# returns 20 as there are 5 x 4 = 20 records



