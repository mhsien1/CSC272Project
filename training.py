# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 20:15:21 2018

@author: Michael
"""
from sklearn.naive_bayes import ComplementNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from random import shuffle
from sklearn import metrics

df = pd.read_csv('nysenate_labeled.csv')
print(df.head(1))


train_data = []

for row in df.itertuples():
    #print(row[4])
    train_data.append((row[3],row[4]))    

print(len(train_data))

vectorizer = CountVectorizer(stop_words = 'english', analyzer='word', min_df = 5, binary = True,max_features = 10000)

#print(train_data[0])
shuffle(train_data)

test_data = train_data[150:]
test_data_tweet =  [ doc for (doc,label) in test_data]
test_data_label = [ label for (doc,label) in test_data] 

#print(len(test_data))
train_data = train_data[:150]
train_data_tweet =  [ doc for (doc,label) in train_data]
train_data_label = [ label for (doc,label) in train_data] 
#print(len(train_data))

count_train_data =  vectorizer.fit_transform(train_data_tweet)  
count_test_data  =  vectorizer.transform(test_data_tweet)

#naive_bayes = GaussianNB()
#naive_bayes = ComplementNB()
naive_bayes = MultinomialNB()
#naive_bayes = BernoulliNB()


nb_classifier = naive_bayes.fit(count_train_data, train_data_label)

result  =  nb_classifier.predict(count_test_data)   
accuracy = nb_classifier.score(count_test_data, test_data_label)

score = metrics.accuracy_score(test_data_label, result)
print("accuracy:   %0.3f" % score)

print("classification report:")
print(metrics.classification_report(test_data_label, result))
print("confusion matrix:")
print(metrics.confusion_matrix(test_data_label, result))

