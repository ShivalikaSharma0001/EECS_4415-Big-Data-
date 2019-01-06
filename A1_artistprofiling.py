# -*- coding: utf-8 -*-
# =============================================================================
# Given a collection of English songs, it computes and prints out (in
# the STDOUT) the profile of each artist/band in the collection; the profile of an 
# artist/band consists of the top-100 more important words of their song lyrics, 
# based on the tf-idf score.Before printing out, you need to sort the pairs of 
# (word, score) in descending order of score
#
# Name: Shivalika Sharma, Komal Arora
#
# =============================================================================

import pandas
import nltk
from nltk.corpus import stopwords 
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import math
from collections import OrderedDict
from itertools import groupby
import sys

# === FUNCTIONS ===

# function to find unique words given the tokens. Also removes the one letter words, words containing "'" and stop words
def find_unique_words(tokens): 
    t = set()
    for a in range(len(tokens)):
        if len(tokens[a]) != 1 and "'" not in tokens[a]:
            t.add(tokens[a])
              
    v = set()
    for c in range(len(t)):
        element = t.pop().lower()
        v.add(element)
        
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in v if not w in stop_words] 
    filtered_sentence = [] 
    for w in v: 
        if w not in stop_words: 
            filtered_sentence.append(w) 
    
    return filtered_sentence # returns the array of unique and clean words 

# similar to above function but does not use set as we do not want to remove duplicates 
def find_words(tokens): 
    t = []
    for a in range(len(tokens)):
        if len(tokens[a]) != 1 and "'" not in tokens[a]:
            t.append(tokens[a])
      
    for c in range(len(t)):
         t[c] = t[c].lower()
         
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in t if not w in stop_words] 
    filtered_sentence = [] 
    for w in t: 
        if w not in stop_words: 
            filtered_sentence.append(w) 
    
    return filtered_sentence # returns array of clean words 

#df = pandas.read_csv('songdata.csv')
# to run the file, "python artistprofiling.py songdata.csv" or uncomment above line 
df = pandas.read_csv(sys.argv[1])

arr = [] # a big array to store all the unique words used in all the lyrics of all the songs
for a in range(len(df['text'])):
    tokens = nltk.word_tokenize(df['text'][a])
    arr = find_unique_words(tokens) + arr

s = set(arr) # a set - to remove duplicate, if exists, from the array arr

art = [len(list(group)) for key, group in groupby(df['artist'])]  # an array of number of songs sung by each artist

dict = {}
count = 0
for i in range(len(art)):
     str = "" # making a string of all the songs sung by an artist
     if i == 0:
        for j in range(art[i]): 
             str = str + df['text'][j]
             dict[i] = str 
     else:
         count = count + art[i-1]
         for j in range(art[i]):
             str = str + df['text'][j+count]
             dict[i] = str 
          
idf = {} # a dictionary which stores the unique words as keys and their idf value as the value
for a in range(len(dict)):
    tokens = nltk.word_tokenize(dict.get(a))
    ar = find_words(tokens) # calling the function to find words 
    for b in range(len(s)): # checking if an item b from the set a exists in array ar
        if list(s)[b] in ar:
            if list(s)[b] in idf:
                idf[list(s)[b]] = idf[list(s)[b]] + 1 # if not the first time, increase the value by 1
            else:
                idf[list(s)[b]] = 1  # if for first time, save the word as key and 1 as the value
    
total_num_singers = len(art)
for a in range(len(idf)): # in order to find idf, divide by 1, multiply by total number of songs and take the log10 of final result in the same idf array
    idf[list(idf)[a]] = 1/idf[list(idf)[a]]
    idf[list(idf)[a]] = idf[list(idf)[a]]*total_num_singers
    idf[list(idf)[a]] = math.log10(idf[list(idf)[a]])
    
for a in range(len(dict)): # this will iterate through all the songs of an artist
    tokens = nltk.word_tokenize(dict.get(a))
    ar = find_words(tokens) # calling function to find words 
    num_words_song_sung_artist = len(ar) # get the length of the array from above 
    tf = {} # create a new array tf
    for b in range(len(ar)): # check if an item b exists in ar, if it does then add it as the key in tf and its num of occurrences as value
        if ar[b] in ar:
            if ar[b] in tf:
                tf[ar[b]] = tf[ar[b]] + 1
            else:
                tf[ar[b]] = 1
    for c in range(len(tf)): # divide by the number of words in the song
        tf[list(tf)[c]] = tf[list(tf)[c]]/num_words_song_sung_artist
    for c in range(len(tf)): # get the final tf-idf value by multiplying tf value with the idf value of the word
        tf[list(tf)[c]] = tf[list(tf)[c]]*idf.get(list(tf)[c])
    sort = OrderedDict(sorted(tf.items(), key=lambda x: x[1], reverse = False)) # sort in decreasing value of tf-idf
    
    print()
    if len(sort) < 100: # if number of words less than 100, print those
        for i in range(len(sort)):
            item = sort.popitem()
            print(item)  
    else:
        for i in range(100): # print top 100 more important words and their tf-idf value
            item = sort.popitem()
            print(item)

    
