#!/usr/bin/python

# -*- coding: utf-8 -*-
# =============================================================================
# 
# Name: Shivalika Sharma, Komal Arora
# 
# =============================================================================

import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt

f = open('result.txt', 'r')
for line in f.readlines():
    x = []
    y = []
    if line != '\n':
        values = line.split('|')
        for a in range(len(values)):
            if values[a] != '\n' and values[a]:
                dict = values[a].split()
                x.append(dict[0])
                y.append(dict[1])
                
                plt.bar(x, y, color='purple', linewidth=2, linestyle='dashed', align='center', alpha=1)
                plt.ylabel('Number of Occurrences')
                plt.title('Hashtags')
                plt.show()
