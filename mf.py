#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test
collection = db.mf
#collection.insert({'time': datetime.datetime(2009, 11, 12)})

#print time.strptime('Tue Dec 05', "%a %b %d")

d = "Thu Dec 05 00:00:00 +0800 1996"

d =  d[0:11] + d[-4:]

d = time.strptime(d, "%a %b %d %Y")

d = datetime.datetime(d.tm_year, d.tm_mon, d.tm_mday)

d2 = datetime.datetime(2012, 1, 1)

if d > d2:
    print 'aaa'
else:
    print 'bbb'

#collection.insert({'date': d})
