#! /usr/bin/python

# -*- coding: utf-8 -*-
# =============================================================================
# 
# compute the number of occurrences of each trigram in the song collection (tmapper.py,
# treducer.py) and output the results in a file called trigrams.txt
# Mapper
# Name: Shivalika Sharma, Komal Arora
# 
# =============================================================================

import re
import sys

def dataCleaning(ar):   #function which removes 1 letter words, non-alpha words and changes all the words to lower case. It also removes our delimiter word
    t = []          
    for a in range(len(ar)):
        if len(ar[a]) != 1 and not re.match("^[0-9]+$", ar[a]) and ar[a].isalpha(): 
            t.append(ar[a].lower().replace("NewSongNow",""))
    return t
    
def removeStopWords(ar):    #function which removes all the stop words from our array
    stop_words = {'out', 'we', 'was', 'how', 'myself', 'for', 'they', 'about', "hasn't", 'then', 'both', 'so', 're', 'don',
 'm', 'as', 'any', 'mightn', 'after', 'you', 'wouldn', 'why', 'been', 'where', 'by', "isn't", 'yourself', 'wasn', 
 'a', "haven't", 'did', "hadn't", 'their', 'hasn', 'doing', 'be', 'further', 'ours', 'now', 'am', 'her', "you'll", 'yourselves',
 'that', 'my', 'what', 'to', 'd', 'not', "won't", "couldn't", 'own', 'there', 'this', 'each', 'all', 'haven', 'more', 'me', 've',
 'weren', 'which', 'himself', 'nor', 'other', "shouldn't", 'who', "should've", 'same', 'at', 'such', 't', 'up', 'than', 'can', "you've", 
 'too', 'these', 'while', "wasn't", 'ourselves', 'before', 'i', 'he', "didn't", 'our', 'its', 'but', 'with', "wouldn't", 'those', 'because', 
 'the', 'y', 'shouldn', 'it', 'mustn', 'hers', 'just', 'doesn', 'ain', 'between', 'over', 'had', 'aren', "mightn't", 'does', 'have', 'and', 'or',
 'some', "mustn't", 'only', 'won', 'when', 'needn', 'below', 'in', 'if', 'theirs', "needn't", "aren't", 'isn', 'again', 'his', 'whom', 'll', 'hadn',
 'above', 'should', 'itself', 'themselves', 'until', 'are', 'she', 'no', 'from', 'into', 'will', 'your', 'few', 'herself', 'of', 'has',
 'down', 'were', 'once', 'ma', 'having', 'them', 'under', 'him', 'shan', 'couldn', 'do', 'on', 'an', "you'd", 'yours', 'being', 'off', 'o',
 "that'll", 'very', "weren't", 'didn', 'through', 
 "you're", 'most', 'against', "it's", "doesn't", 'here', 'is', 's', "don't", "shan't", 'during', "she's"}
    filtered_sentence = [w for w in ar if not w in stop_words] 
    filtered_sentence = [] 
    for w in ar: 
        if w not in stop_words: 
            filtered_sentence.append(w) # array of unique, clean words 
    return filtered_sentence
    
def removeUnwantedWords(ar):    #function which removes unwanted words like chorus, verse etc from our array
    while 'chorus' in ar:
        ar.remove('chorus')
        
    while 'verse' in ar:
        ar.remove('verse')
        
    while 'pre-chorus' in ar:
        ar.remove('pre-chorus')
        
    return ar
        
def clean(ar):  #the clean function which alls the following sub-functions in sequence
    t = dataCleaning(ar)
    u = removeStopWords(t)
    v = removeUnwantedWords(u)
    return v

for line in sys.stdin:  #reading line by line from sys.stdin
    line = re.sub(r'^\W+|\W+$', '', line)   #takes off non-words
    songs = line.split("NewSongNow")    #split songs with the delimiter word NewSongNow and put each song into an array called songs
    
    for a in range(len(songs)): #iterating through all the songs one by one
        count = len(songs)  #count of the number of songs
        if a != 0 and a < count-1:  #this will skip the title of songs column i.e. text and go until the last song
            wordArr = []    #another array for storing the words of each song
            wordArr.append(songs[a].split())    #split method to get words out of a line
    
            cleanArr = []   #array to get the clean words of each song
            for a in range(len(wordArr)):   #iterating through all the songs
                cleanArr = clean(wordArr[a])    #calling the function clean and sending one song's array to it
                
    for i in range(len(cleanArr)):  #iterating through the clean array
         if (i < len(cleanArr)-2):  #this will stop at the third last word of the array
              print("%s %s %s\t%s" % (cleanArr[i], cleanArr[i+1], cleanArr[i+2], 1))    #pritning out the final answer
                 
