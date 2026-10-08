# Creating RDDs from a Text File or Files

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import count
from pyspark import SparkContext

sc = SparkContext()

##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# sc.textFile(name, minPartitions=None, use_unicode=True)
##### ##### ##### ##### ##### ##### ##### ##### ##### #####

kvpairs = sc.parallelize([('city','Hayward')
                         ,('state','CA')
                         ,('zip',94541)
                         ,('country','USA')])
print(kvpairs.keys().collect())
# returns ['city', 'state', 'zip', 'country']


print(kvpairs.values().collect())
# returns ['Hayward', 'CA', 94541, 'USA']



locations = sc.parallelize([('Hayward', 'USA', 1)
                           ,('Baumholder','Germany', 2)
                           ,('Alexandria','USA', 3)
                           ,('Melbourne','Australia', 4)])
bylocno = locations.keyBy(lambda x: x[2])
print(bylocno.collect())
# returns:
#[(1, ('Hayward', 'USA', 1)), (2, ('Baumholder', 'Germany', 2)),
# (3, ('Alexandria', 'USA', 3)), (4, ('Melbourne', 'Australia', 4))]



locwtemps = sc.parallelize(['Hayward,71|69|71|71|72',
                            'Baumholder,46|42|40|37|39',
                            'Alexandria,50|48|51|53|44',
                            'Melbourne,88|101|85|77|74'])
kvpairs = locwtemps.map(lambda x: x.split(','))
print(kvpairs.take(4))
# returns :
# [['Hayward', '71|69|71|71|72'],
# ['Baumholder', '46|42|40|37|39'],
# ['Alexandria', '50|48|51|53|44'],
# ['Melbourne', '88|101|85|77|74']]

locwtemplist = kvpairs.mapValues(lambda x: x.split('|')) \
                      .mapValues(lambda x: [int(s) for s in x])
print(locwtemplist.take(4))
# returns :
# [('Hayward', [71, 69, 71, 71, 72]),
# ('Baumholder', [46, 42, 40, 37, 39]),
# ('Alexandria', [50, 48, 51, 53, 44]),
# ('Melbourne', [88, 101, 85, 77, 74])]

locwtemps = kvpairs.flatMapValues(lambda x: x.split('|')) \
                   .map(lambda x: (x[0], int(x[1])))
print(locwtemps.take(3))
# returns :
# [('Hayward', 71), ('Hayward', 69), ('Hayward', 71)]



print("")
print("")
print("")

# continued from Listing 4.29
grouped = locwtemps.groupByKey()
print(grouped.take(1))
# returns:
# [('Melbourne', <pyspark.resultiterable.ResultIterable object at 0x7f121ce11390>)]

avgtemps = grouped.mapValues(lambda x: sum(x)/len(x))
print(avgtemps.collect())
# returns:
# [('Melbourne', 85), ('Baumholder', 40), ('Alexandria', 49), ('Hayward', 70)]

#(71,1), (69,1), (71,1)  
#x       y  => (140, 2)  
temptups = locwtemps.mapValues(lambda x: (x, 1))
# creates tuples (city, (temp, 1))
inputstoavg = temptups.reduceByKey(lambda x, y: (x[0]+y[0], x[1]+y[1]))
print(inputstoavg.take(4))
print("******")
print("")

'''
# sums temperatures by city
averages = inputstoavg.map(lambda x: (x[0], x[1][0]/x[1][1]))
# divides the sum of temperatures by key by the number of readings
print(averages.take(4))
# returns :
# [('Baumholder', 40.8),
# ('Melbourne', 85.0),
# ('Alexandria', 49.2),
# ('Hayward', 70.8)]




maxbycity = locwtemps.foldByKey(0, lambda x, y: x if x > y else y)
print(maxbycity.collect())
# returns :
# [('Baumholder', 46), ('Melbourne', 101), ('Alexandria', 53),('Hayward', 72)]



sortedbykey = locwtemps.sortByKey()
print(sortedbykey.take(4))
# returns:
# [('Alexandria', 50), ('Alexandria', 48), ('Alexandria', 51),('Alexandria', 53)]

sortedbyval = locwtemps.map(lambda x: (x[1],x[0])) \
                       .sortByKey(ascending=False)
print(sortedbyval.take(4))
# returns:
# [(101, 'Melbourne'), (88, 'Melbourne'), (85, 'Melbourne'), (77,'Melbourne')]

'''

