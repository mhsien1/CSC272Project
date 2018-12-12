# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 21:33:52 2018

@author: Michael
"""

from TwitterAPI import TwitterAPI
import pandas as pd
import csv

query = 'Gillibrand'
PRODUCT = 'fullarchive'
LABEL = 'Testing'

api = TwitterAPI("nWQzqafsC0XcH370OkSlwxonQ", 
             "ZZWqC0b1hO3N8bGO5yfpTj98mnptVBTJX6sZ9fbBdBmH9h0SUJ", 
             "706273045527314432-GymkKoqae8a3uNBSALfjG2pcnr6oT34", 
             "EUQ40A65Bck7yVQceSClcGX3Q3eKvNSVq3VXCZk1o7yBq")

csvFile = open('Gillibrand.csv', 'a',encoding="utf-8")
csvWriter = csv.writer(csvFile)

tnext = ' '
i = 0
r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL), 
        {'query':query, 
         'fromDate':'201809010000',
         'toDate':'201811052200'
         }
        )

for item in r:
    csvWriter.writerow([item['created_at'],item['user']['screen_name'], item['text'] if 'text' in item else item])
json = r.json()
if 'next' not in json:
    print("fail")
tnext = json['next']

while(i<15):
    r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL), 
        {'query':query, 
         'fromDate':'201809010000',
         'toDate':'201811052200','next':tnext
         }
        )
    if r.status_code != 200:
        break
    for item in r:
        csvWriter.writerow([item['created_at'],item['user']['screen_name'], item['text'] if 'text' in item else item])
    json = r.json()
    if 'next' not in json:
        break
    tnext = json['next']
    i+= 1
print("finish")