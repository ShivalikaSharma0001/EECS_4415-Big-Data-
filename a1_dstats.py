# -*- coding: utf-8 -*-
# =============================================================================
# Write a python program (dstats.py) that given a collection of English song lyrics computes and
# prints out (in the STDOUT) the following statistics:
# 1. number of artists/bands in the collection (numOfArtists)
# 2. number of songs in the collection (numOfSongs)
# 3. average number of songs per artist/band (avgNumOfSongs)
# 4. average number of unique words per song in the collection (avgNumOfWords)
# 5. average number of unique words per song of an artist/band, sorted by artist/band name in an
# alphanumerically ascending order, i.e., a->z (pairsOfArtistAvgNumOfWords)
# plot a bar chart that shows the top-10 pairs found in the previous bullet, where the x-axis
# represents the artists/band and the y-axis represents the average number of words.
#
# Name: Shivalika Sharma, Komal Arora
# 
# =============================================================================

import pandas
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
from itertools import groupby
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import sys

# === FUNCTIONS === 

# This function finds num of unique words. It also removes 1-length words,
# words consisting of ' and stop words from the set
# It takes in tokens and return the count of words
def find_num_unique_words_for_avgNumOfWords(tokens): 
    t = set() # set to remove duplicates 
    for a in range(len(tokens)):
        for b in range(len(tokens[a])):
            if len(tokens[a][b]) != 1 and "'" not in tokens[a][b]: 
                t.add(tokens[a][b])
                
    v = set()
    for c in range(len(t)): # converting the words to lower case so that they can be comapred with stop words which are also in lower case
        element = t.pop().lower()
        v.add(element)
        
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in v if not w in stop_words] 
    filtered_sentence = [] 
    for w in v: 
        if w not in stop_words: 
            filtered_sentence.append(w) # array of unique, clean words 
    
    return len(filtered_sentence) # return the length of the array

# similar to find_num_unique_words_for_avgNumOfWords(tokens)
# The difference between this function and the one above is in the way data being extracted from tokens
def find_num_unique_words_for_pairsOfArtistAvgNumOfWords(tokens): 
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
    
    return len(filtered_sentence)

df = pandas.read_csv('final.csv')
# to run the file, "python dstats.py songdata.csv" or uncomment above line 
#df = pandas.read_csv(sys.argv[1])

# number of artists/bands in the collection (numOfArtists) #
s = set(df['artist'])
numOfArtists = len(s)
print("number of artists/bands in the collection (numOfArtists)", numOfArtists)

# number of songs in the collection (numOfSongs) #
numOfSongs = df.shape[0]  # gives number of row count
print("number of songs in the collection (numOfSongs)", numOfSongs)

# average number of songs per artist/band (avgNumOfSongs) #
avgNumOfSongs = numOfSongs/numOfArtists
print("average number of songs per artist/band (avgNumOfSongs)", avgNumOfSongs)

# average number of unique words per song in the collection (avgNumOfWords) #
df['text'].dropna(inplace=True)
tokens = df['text'].apply(word_tokenize)
  
avgNumOfWords = find_num_unique_words_for_avgNumOfWords(tokens)/numOfSongs
print("average number of unique words per song in the collection (avgNumOfWords)", avgNumOfWords)

# average number of unique words per song of an artist/band, sorted by artist/band name in an
# alphanumerically ascending order, i.e., a->z (pairsOfArtistAvgNumOfWords) #
a = [len(list(group)) for key, group in groupby(df['artist'])]

print("average number of unique words per song of an artist/band, sorted by artist/band name in analphanumerically ascending order, i.e., a->z (pairsOfArtistAvgNumOfWords)")
count = 0
x_axis = []
y_axis = []
for i in range(len(a)):
    num = 0;
    tokens = "";
    if i == 0:
        for j in range(a[i]):
             tokens = nltk.word_tokenize(df['text'][j])
             num = num + find_num_unique_words_for_pairsOfArtistAvgNumOfWords(tokens)
        x_axis.append(df['artist'][0])
        y_axis.append(num/a[i])
        print(df['artist'][0], num/a[i])
    else:
         count = count + a[i-1]
         for j in range(a[i]):
             tokens = nltk.word_tokenize(df['text'][j+count])
             num = num + find_num_unique_words_for_pairsOfArtistAvgNumOfWords(tokens)
         x_axis.append(df['artist'][count])
         y_axis.append(num/a[i])
         print(df['artist'][count], num/a[i])
        
# plot a bar chart that shows the top-10 pairs found in the previous bullet, where the x-axis
# represents the artists/band and the y-axis represents the average number of words. Note that
# the top-1 artist/band is the one with the largest average number of unique words per song. #
x = []
y = []
for i in range(2):
    x.append(x_axis[i])
    y.append(y_axis[i])
    
#x_axis = np.arange(len(x_axis))
#plt.bar(x_axis, y_axis, align='center', alpha=0.5)
plt.bar(x, y, align='center')
#plt.xticks()
plt.ylabel('average number of words')
plt.title('artists/bands')
plt.show()

