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

lowercase = words.map(lambda x: x.lower())

allwords = lowercase.count()
distinctwords = lowercase.distinct().count()
print "Total words: %s, Distinct Words: %s" % (allwords, distinctwords)
# returns Total words: 81282049, Distinct Words: 2803281

words = logs.flatMap(lambda x: x.split(' ')) \
            .filter(lambda x: len(x) > 0)
groupedbyfirstletter = words.groupBy(lambda x: x[0].lower())
print(groupedbyfirstletter.take(5))



# creating RDD x with words
x = sc.parallelize(["Joseph", "Jimmy", "Tina", 
                    "Thomas", "James", "Cory",
                    "Christine", "Jackeline", "Juan"], 3)
 
# Applying groupBy operation on x
y = x.groupBy(lambda word: word[0])
 
for t in y.collect():
    print((t[0],[i for i in t[1]]))
 
# ('J', ['Joseph', 'Jimmy', 'James', 'Jackeline', 'Juan'])
# ('C', ['Cory', 'Christine'])
# ('T', ['Tina', 'Thomas'])


sortbyfirstletter = x.sortBy(lambda x: x.lower(), ascending=False)
print(sortbyfirstletter.take(10))
print(sortbyfirstletter.collect())

