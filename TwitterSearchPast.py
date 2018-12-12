# Handler to get tweets using Twitter's premium search + twitter API
# Is able to get tweets from any time period


from TwitterAPI import TwitterAPI
import pandas as pd
import csv

# query is what you want to search for
# Label is the name of your dev environment
query = 'Gillibrand'
PRODUCT = 'fullarchive'
LABEL = 'Testing'

# To use twitter API you must provide secret keys in the following order
# consumer secret, consumer secret key, access token, access token secret
api = TwitterAPI("nWQzqafsC0XcH370OkSlwxonQ", 
             "ZZWqC0b1hO3N8bGO5yfpTj98mnptVBTJX6sZ9fbBdBmH9h0SUJ", 
             "706273045527314432-GymkKoqae8a3uNBSALfjG2pcnr6oT34", 
             "EUQ40A65Bck7yVQceSClcGX3Q3eKvNSVq3VXCZk1o7yBq")

# write the data into a csv file so that processing the data later is easier

csvFile = open('Gillibrand.csv', 'a',encoding="utf-8")
csvWriter = csv.writer(csvFile)

# the initial api request
# dates are in YYYYMMDDHHMM format
# both from date and to date are used to fix the date range of the tweets to before the end of the
# midterm elections
# tnext is initially not used
tnext = ' '
i = 0
r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL), 
        {'query':query, 
         'fromDate':'201809010000',
         'toDate':'201811052200'
         }
        )
		
#write each tweet into a different row in the csv
for item in r:
    csvWriter.writerow([item['created_at'],item['user']['screen_name'], item['text'] if 'text' in item else item])
json = r.json()
if 'next' not in json:
    print("fail")
# tnext stores the next set of tweets if one requestdoes not get all of them
tnext = json['next']

# limits the amount of requests because the api only allows for a certain amount of requests per day
# breaks the loop in case of error with request or there are no more tweets left to get
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