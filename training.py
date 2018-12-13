# Main function to train classifier
# Uses sklearn library and is able to work for various naive_bayes classifieres

from sklearn.naive_bayes import ComplementNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from random import shuffle
from sklearn import metrics
import collections
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# location of the csv file that contains labeled data
df = pd.read_csv('nysenate_labeled.csv')
df2 = pd.read_csv('election2018.csv')
df3 = pd.read_csv('farley_labeled.csv')
# used doublecheck the format of the given csv file
print(df.head(1))
print(df2.head(1))
print(df3.head(1))

#store all data into train_data
train_data = []

# iterate through each row of the csv file 
# append to train_data a tuple containing the (tweet,label)
# possible labels are democratic, republican , and indifferent

for row in df.itertuples():
    #print(row[4])
    train_data.append((row[3],row[4]))    

for row in df2.itertuples():
    #print(row[4])
    train_data.append((row[3],row[4]))    

for row in df3.itertuples():
    #print(row[4])
    train_data.append((row[3],row[4])) 

# Stop word remove the most common words in the english language
# minimum document frequency is 5, meaning a word must appear in 5 seperate tweets to be considered
vectorizer = CountVectorizer(stop_words = 'english', analyzer='word', min_df = 5, binary = True,max_features = 10000)

# Shuffles the training data.
shuffle(train_data)

print(len(test_data))

# takes the first x tweets to be used as to train the classifier
# seperates the tweets and the labels
x = 300
test_data = train_data[x:]
test_data_tweet =  [ doc for (doc,label) in test_data]
test_data_label = [ label for (doc,label) in test_data] 

#print(len(test_data))

# takes the last x tweets to be used as to test how well the classifier works
# seperates the tweets and the labels
train_data = train_data[:x]
train_data_tweet =  [ doc for (doc,label) in train_data]
train_data_label = [ label for (doc,label) in train_data] 
#print(len(train_data))

#Copy the tweets for the final set of all tweets
total_data = []
total_data = total_data + test_data_tweet
total_data = total_data + train_data_tweet

#print(total_data)
#transformo data using the vectorizer
count_train_data =  vectorizer.fit_transform(train_data_tweet)  
count_test_data  =  vectorizer.transform(test_data_tweet)



# Several differnt NB algoithms can be used just switch out which one you want to test
#naive_bayes = GaussianNB()
#naive_bayes = ComplementNB()
naive_bayes = MultinomialNB()

# use selected algorithm to fit the data.
nb_classifier = naive_bayes.fit(count_train_data, train_data_label)

# compares the preditcted labels against the actual labels then prince th accuracy.
# also prints out detailed classification report 
result  =  nb_classifier.predict(count_test_data)   
accuracy = nb_classifier.score(count_test_data, test_data_label)

score = metrics.accuracy_score(test_data_label, result)
print("accuracy:   %0.3f" % score)

print("classification report:")
print(metrics.classification_report(test_data_label, result))

#Prints out the confusion_matrix
print("confusion matrix:")
print(metrics.confusion_matrix(test_data_label, result))


df5 = pd.read_csv('farley.csv')
df6 = pd.read_csv('Gillibrand.csv')

for row in df5.itertuples():
    total_data.append(row[3])    

for row in df6.itertuples():
    total_data.append(row[3])    

count_total_data  =  vectorizer.transform(total_data)

final_result = nb_classifier.predict(count_total_data)   
counter =(collections.Counter(final_result))
print(counter)
print(counter['dem'])

x = ['Dem','Rep','Neu']
y_pos = np.arange(len(x))
amount = [counter['dem'],counter['rep'],counter['ind']]
plt.title("Twitter Political Leanings")
plt.bar(y_pos,amount,align='center', alpha=0.5)
plt.xticks(y_pos, x)
plt.ylabel('tweets')
plt.show()

labels = ['Dem','Rep']
sizes = [counter['dem'],counter['rep']]
#explode = (0.1, 0, 0, 0)  # explode 1st slice
 
# Plot
plt.pie(sizes,labels=labels,
        autopct='%1.1f%%', shadow=True, startangle=140)
 
plt.axis('equal')
plt.show()