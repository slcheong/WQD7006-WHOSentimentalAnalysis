# -*- coding: utf-8 -*-
"""
Created on Fri May 15 09:09:43 2020

@author: Soon Loong
"""

import pandas as pd
import re

# Importing the training set
df = pd.read_csv('output.csv')



def removeB(x):
    temp = x
    temp = re.sub("^b\'|^b\"|\'$|\"$"," ",temp)
    return temp

def removeSlashChar(x):
    temp = x
    temp = re.sub(r"\\\w+"," ",temp)
    return temp  
    
def removeURL(x):
    temp = x
    #remove url
    temp = re.sub(r'https:\/\/.*[\r\n]*', ' ', temp, flags=re.MULTILINE)
    return temp

def removeHTMLChar(x):
    temp = x
    string = ["&amp;"]
    for a in string:
        temp = re.sub(a, ' ', temp)
    return temp
    
def removeAlliance(x):
    temp = x
    temp = re.sub(r'@\w+', ' ', temp)
    return temp
    
def removeHashTag(x):
    temp = x
    temp = re.sub(r'#\w+', ' ', temp)
    return temp




df['Author'] = df['Author'].apply(lambda x: removeB(x))

df['Location'] = df['Location'].apply(lambda x: removeB(x))
df['Location'] = df['Location'].apply(lambda x: removeSlashChar(x))

df['Text'] = df['Text'].apply(lambda x: removeB(x))
df['Text'] = df['Text'].apply(lambda x: removeURL(x))
df['Text'] = df['Text'].apply(lambda x: removeSlashChar(x))

df['Text'] = df['Text'].apply(lambda x: removeHTMLChar(x))
df['Text'] = df['Text'].apply(lambda x: removeAlliance(x))
#df['Text'] = df['Text'].apply(lambda x: removeHashTag(x))
df = df.drop_duplicates(subset='Text',keep='first')


x = df['Text'][8]
x1 = removeAlliance(x)