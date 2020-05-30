# -*- coding: utf-8 -*-
"""
Created on Mon May 11 09:46:20 2020

@author: Soon Loong
"""

#pass twitter credentials to tweepy

import tweepy
import csv


consumer_key = ''
consumer_secret = ''
access_token= ''
access_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

csvFile = open('output2.csv', 'a')
csvWriter = csv.writer(csvFile)

search_terms = '#WHO OR #WorldHealthOrganization OR #TedrosAdhanom -filter:retweets'

for status in tweepy.Cursor(api.search,
                       q=search_terms,
                       since='2020-05-03', until='2020-05-10',
                       result_type='mixed',
                       tweet_mode = 'extended',
                       include_entities=True,
                       monitor_rate_limit=True, 
                       wait_on_rate_limit=True,
                       lang="en").items():

    csvWriter.writerow([status.created_at, status.user.screen_name.encode('utf8'),status.user.location.encode('utf8'), status.full_text.encode('utf-8')])

csvFile.close()