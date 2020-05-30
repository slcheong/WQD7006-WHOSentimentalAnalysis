# -*- coding: utf-8 -*-
"""
Created on Thu May 28 21:29:56 2020

@author: Soon Loong
"""

import pandas as pd
import numpy as np

#read csv
df = pd.read_csv("Annotated.csv")

# Remove not relevant tweets
df = (df[df["Remark"] != 'x'])

# Remove not relevant columns
df = df.drop(["No","Remark"], axis = 1)

# Remove leading space in author
def removeLeadingSpace(x):
    temp = x
    temp = temp.lstrip()
    return temp


df["Author"] = df["Author"].apply(lambda x: removeLeadingSpace(x))

#Clean Location
def cleanLocation(x):
    temp = x
    arr = temp.split(",")
    text = arr[-1]
    text = text.lstrip()
    if text == "":
        text = "Others"
    return text

df["Location"] = df["Location"].apply(lambda x: cleanLocation(x))


#Clean Text
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download('stopwords')
all_stopwords = stopwords.words('english')
ps = PorterStemmer()

        
def cleanText(x):
    temp = x
    #retain alphabet only
    temp = re.sub("[^a-zA-Z]"," ",temp)
    #change all word to lower case
    temp = temp.lower()
    
    #split tweet into list 
    tweet_arr = temp.split()
    
    #Remove stop words and stem words
    tweet_arr = [ps.stem(word) for word in tweet_arr if not word in set(all_stopwords)]
    tweet_arr = [word for word in tweet_arr if len(word) > 1]
    tweet_arr = ' '.join(tweet_arr)
    return tweet_arr
    
df["CleanText"] = df["Text"].apply(lambda x: cleanText(x))


##Create Bag of Words CSV
from sklearn.feature_extraction.text import CountVectorizer

#Create X
cv = CountVectorizer(max_features=1000)
'''
In case we want to limit X to improve training speed, replace line above with below
cv = CountVectorizer(max_features=2000)
'''
corpus = df["CleanText"].to_numpy()
X = cv.fit_transform(corpus).toarray()

# Create Y
y = df["Annotate"].values

# Join X & Y to form new array to convert to df1
y = y.reshape((y.shape[0],1))
z = np.append(X,y,axis =1)
col_name = cv.get_feature_names()
col_name.append("Sentimen")
df1 = pd.DataFrame(z,columns = col_name)

## Save to CSV file
pd.DataFrame(z,columns = col_name).to_csv("bagOfWords1000.csv",index=False)


## EDA ##

#Numer of Tweet per Author
df["Author"].value_counts()

#Number of Tweet per Location
df["Location"].value_counts()


## Create Word Cloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt 

words = ""
for i in corpus:
    words += " "+i+" "
    
    
wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = all_stopwords, 
                min_font_size = 10).generate(words) 
  
# plot the WordCloud image                        
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show() 
