#! /usr/bin/python

# -*- coding: utf-8 -*-
# =============================================================================
# 
# compute the number of occurrences of each trigram in the song collection (tmapper.py,
# treducer.py) and output the results in a file called trigrams.txt
# Reducer
# Name: Shivalika Sharma, Komal Arora
# 
# =============================================================================

import sys

#initializing the varibales as Nones and 0s, wordsCur and last are strings and counts are ints
wordCur = None 
wordLast = None
wordCurCount = 0
count = 0

for line in sys.stdin:  #reading the file input from sys.stdin
    line = line.strip() #removes leading and trailing characters 
    wordCur, count = line.split('\t', 1)    #splitting the line with the delimiter tab

    try:
        count = int(count)  #converting the count to an int
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    if wordCur == wordLast:
        wordCurCount = wordCurCount + count #if two consecutive words are the same, increase the count
    else:
        if wordLast:    
            print('%s\t%s' % (wordLast, wordCurCount))  #printing the result
        
        wordCurCount = count #resetting the values, for count to be the last count
        wordLast = wordCur # and for word to be the last word

if wordLast == wordCur:
    print ('%s\t%s' % (wordLast, wordCurCount)) #prting the result when two consecutive words found