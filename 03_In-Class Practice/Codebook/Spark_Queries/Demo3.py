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
# 1. sample json
##### ##### ##### ##### ##### ##### ##### ##### ##### #####
people = spark.read.json("file:///home/kunwu/data/sampledata/people.json")

print(type(people))
print(people)
print(people.dtypes)
people.show()


##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# 2. zipcodes.json
##### ##### ##### ##### ##### ##### ##### ##### ##### #####
zipcodes = spark.read.json("file:///home/kunwu/data/sampledata/all_zipcodes.json")
print(type(zipcodes))
print(zipcodes)
print(zipcodes.dtypes)
zipcodes.show()

'''
##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# 3. multiline json
##### ##### ##### ##### ##### ##### ##### ##### ##### #####
multiline_df = spark.read.option("multiline",True) \
      .option("mode", "PERMISSIVE") \
      .json("file:///home/kunwu/data/sampledata/multiline-zipcode.json")
multiline_df.show()



##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# 4. multiple json files
##### ##### ##### ##### ##### ##### ##### ##### ##### #####
df2 = spark.read.json(
    ['file:///home/kunwu/data/zipcodes1.json','file:///home/kunwu/data/sampledata/zipcodes2.json'])
df2.show()    

##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# 5. read all json files from a directory
##### ##### ##### ##### ##### ##### ##### ##### ##### #####
df3 = spark.read.json("file:///home/kunwu/data/sampledata/zipcodes*.json")
df3.show()
'''
