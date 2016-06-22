#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import tushare

client = MongoClient('localhost', 27017)
db = client.gupiao
collection = db.stock


stock1 = db.stock.find_one({'code': 'SZ000005'})
stock2 = db.stock.find_one({'code': 'SH600651'})

time1 = stock1['start_time']
time2 = stock2['start_time']

timeDiff = time1 - time2
print type(timeDiff.days)
