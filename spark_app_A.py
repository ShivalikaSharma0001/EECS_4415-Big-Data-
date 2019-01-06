#!/usr/bin/python

# -*- coding: utf-8 -*-
# =============================================================================
# 
# Name: Shivalika Sharma, Komal Arora
# 
# =============================================================================

from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
import os

# adding the count of each hashtag to its last count
def aggregate_tags_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)

# process a single time interval
def process_interval(time, rdd):
    # print a separator
    print("----------- %s -----------" % str(time))
    try:
        # sort counts (desc) in this time instance and take top 10
        sorted_rdd = rdd.sortBy(lambda x:x[1], True)
        top10 = sorted_rdd.take(10)

        # print it nicely
        f.write('\n')
        for tag in top10:
            print('{:<40} {}'.format(tag[0], tag[1]))
            f.write('{:<40} {}'.format(tag[0], tag[1]))
            f.write('|')
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)

# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp")
# create spark context with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# create the Streaming Context from spark context, interval size 2 seconds
ssc = StreamingContext(sc, 2)
# setting a checkpoint for RDD recovery (necessary for updateStateByKey)
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 9009
dataStream = ssc.socketTextStream("twitter",9009)

# split each tweet into words
words = dataStream.flatMap(lambda line: line.split(" "))

# filter the words to get only hashtags
#hashtags = words.filter(lambda w: '#' in w)
imp = ['#bitcoin','#cryptocurrency','#crypto','#blockchain','#btc']
hashtags = words.filter(lambda w: w in imp)                
                
#map each hashtag to be a pair of (hashtag,1)
hashtag_counts = hashtags.map(lambda x: (x, 1))

# do the aggregation, note that now this is a sequence of RDDs
hashtag_totals = hashtag_counts.updateStateByKey(aggregate_tags_count)

if os.path.exists("result.txt"):
  os.remove("result.txt")
#  print("File deleted")
f= open("result.txt","w+") 
# do this for every single interval
hashtag_totals.foreachRDD(process_interval)

# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()