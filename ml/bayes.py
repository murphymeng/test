#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
import requests
from pymongo import MongoClient
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
from sklearn import tree
clf = tree.DecisionTreeClassifier(min_samples_split=40)

client = MongoClient('localhost', 27017)
db = client.gupiao
collection = db.day

start_time = datetime.datetime(2013, 4, 16)
end_time = datetime.datetime(2014, 5, 11)

rows = db.day.find({
    'symbol': 'SZ300008',
    'time': {'$gt': start_time, '$lt': end_time}
})

features_train = []
labels_train = []

i = 0
for row in rows:
  if i > 0:
    labels_train.append( row['close'] - row['open'] > 0 )
  if i != rows.count() - 1:
    features_train.append([row['volume_rate'] > 2])
  i += 1


print len(labels_train)
print len(features_train)

clf.fit(features_train, labels_train)


start_time = datetime.datetime(2014, 5, 16)
end_time = datetime.datetime(2015, 5, 11)

rows = db.day.find({
    'symbol': 'SZ300008',
    'time': {'$gt': start_time, '$lt': end_time}
})

features_test = []
labels_test = []

i = 0
for row in rows:
  if i > 0:
    labels_test.append( row['close'] - row['open'] > 0 )
  if i != rows.count() - 1:
    features_test.append([row['volume_rate']])
  i += 1

print clf.score(features_test,labels_test)