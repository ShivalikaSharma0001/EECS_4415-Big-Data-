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
from textblob import TextBlob
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

t1 = 'Google'
t2 = 'Apple'
t3 = 'Microsoft'
t4 = 'IBM'
t5 = 'Adobe'

t1_values = ["#googlemaps","#googledoodle","#chrome", "#googleplay","#android","#chromecast","#youtube","#pixel3","#google","#googlearts"]
t2_values = ["#iOS","#iPhone","#applewatch","#macbook","#ipod","#airpods","#ipad","#itunes","#icloud","#applepay"]
t3_values = ["#azure","#office365","#windows","#xbox","#skype","#microsoftedge","#msn","#onedrive","#cortana","#minecraft"]
t4_values = ["#ibmcloud","#ibmwatson","#ibmsystems","#db2","#bluemix","#watsonsupplychain","#websphere","#ibminternhack","#ibmconsulting"]
t5_values = ["#acrobatpro","#dreamweaver","#adobemuse","#photoshop","#adobedimension","#adoberemix","#framemaker","#robohelp","captivateprime"]


def computeTopic(tweet):
    words = tweet.split(" ")
    for word in words:
        word = word.lower()
        if (len(word) > 1 and word[0] == '#'):
             if word in t1_values:
                 return t1
             elif word in t2_values:
                 return t2
             elif word in t3_values:
                 return t3
             elif word in t4_values:
                 return t4
             elif word in t5_values:
                 return t5
        return ("Unwanted hashtags")

topic_1_positive = 0
topic_2_positive = 0
topic_3_positive = 0
topic_4_positive = 0
topic_5_positive = 0
topic_1_neutral = 0
topic_2_neutral = 0
topic_3_neutral = 0
topic_4_neutral = 0
topic_5_neutral = 0
topic_1_negative = 0
topic_2_negative = 0
topic_3_negative = 0
topic_4_negative = 0
topic_5_negative = 0
    
def computeForGraph(topic, polarity):
    
    if topic == t1:
        if polarity == 1:
            topic_1_positive = topic_1_positive + 1
            f.write('{:<40} {}'.format(topic, topic_1_positive))
        elif polarity == 0:
            topic_1_neutral = topic_1_neutral + 1
            f.write('{:<40} {}'.format(topic, topic_1_neutral))
        elif polarity == -1:
            topic_1_negative = topic_1_negative + 1
            f.write('{:<40} {}'.format(topic, topic_1_negative))
    elif topic == t2:
        if polarity == 1:
            topic_2_positive = topic_2_positive + 1
            f.write('{:<40} {}'.format(topic, topic_2_positive))
        elif polarity == 0:
            topic_2_neutral = topic_2_neutral + 1
            f.write('{:<40} {}'.format(topic, topic_2_neutral))
        elif polarity == -1:
            topic_2_negative = topic_2_negative + 1
            f.write('{:<40} {}'.format(topic, topic_2_negative))
    elif topic == t3:
        if polarity == 1:
            topic_3_positive = topic_3_positive + 1
            f.write('{:<40} {}'.format(topic, topic_3_positive))
        elif polarity == 0:
            topic_3_neutral = topic_3_neutral + 1
            f.write('{:<40} {}'.format(topic, topic_3_neutral))
        elif polarity == -1:
            topic_3_negative = topic_3_negative + 1
            f.write('{:<40} {}'.format(topic, topic_3_negative))
    elif topic == t4:
        if polarity == 1:
            topic_4_positive = topic_4_positive + 1
            f.write('{:<40} {}'.format(topic, topic_4_positive))
        elif polarity == 0:
            topic_4_neutral = topic_4_neutral + 1
            f.write('{:<40} {}'.format(topic, topic_4_neutral))
        elif polarity == -1:
            topic_4_negative = topic_4_negative + 1
            f.write('{:<40} {}'.format(topic, topic_4_negative))
    elif topic == t5:
        if polarity == 1:
            topic_5_positive = topic_5_positive + 1
            f.write('{:<40} {}'.format(topic, topic_5_positive))
        elif polarity == 0:
            topic_5_neutral = topic_5_neutral + 1
            f.write('{:<40} {}'.format(topic, topic_5_neutral))
        elif polarity == -1:
            topic_5_negative = topic_5_negative + 1
            f.write('{:<40} {}'.format(topic, topic_5_negative))
    
    
    
def computePolarity(rdd):
    tweets = rdd.collect()
    polarity = 0

    for one_tweet in tweets:
        analysis = TextBlob(one_tweet) 
        if analysis.sentiment.polarity > 0: 
            polarity = 1 #positive
        elif analysis.sentiment.polarity == 0: 
            polarity = 0 #neutral
        else: 
            polarity = -1 #negative
        topic = computeTopic(one_tweet)
        
        computeForGraph(topic, polarity)
                  
##map each hashtag to be a pair of (hashtag,1)
#hashtag_counts = hashtags.map(lambda x: (x, 1))
#
## do the aggregation, note that now this is a sequence of RDDs
#hashtag_totals = hashtag_counts.updateStateByKey(aggregate_tags_count)
        
        
#        print(polarity, topic)
        
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
f= open("temp.txt","w+")
dataStream = ssc.socketTextStream("twitter",9009)

# split each tweet into words
lines = dataStream.flatMap(lambda line: line.split("\n"))
#words = lines.flatMap(lambda line: line.split(" "))
#lines.foreachRDD(computeTopic)
lines.foreachRDD(computePolarity)
#
if os.path.exists("result_B.txt"):
  os.remove("result_B.txt")
#  print("File deleted")
f= open("result_B.txt","w+") 
# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()


