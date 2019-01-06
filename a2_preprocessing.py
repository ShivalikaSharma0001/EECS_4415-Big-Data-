#! /usr/bin/python

# -*- coding: utf-8 -*-
# =============================================================================
# 
# Pre-processing script, stores songs text from the given csv file
# Delimited every song with the word NewSongNow
# 
# Name: Shivalika Sharma, Komal Arora
# 
# =============================================================================

import csv 
import sys

def process():
    f= open("temp.txt","w+")    #opening a text file to write
    for row in csv.reader(iter(sys.stdin.readline, '')):    #reading line by line from sys.stdin
        f.write(row[3].replace("\n",""))    #removing all new lines
        f.write("NewSongNow")   #adding the NewSongNow string at the end of every song to differentiate two songs

process()   #calling process function 
         
