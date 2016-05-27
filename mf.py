#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test
collection = db.mf
#collection.insert({'time': datetime.datetime(2009, 11, 12)})

d = "Thu Dec 05 00:00:00 +0800 1996"

print time.strptime(d, "%a %b %d %H:%M:%S %z %Y")
