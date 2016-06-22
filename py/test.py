#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
import requests
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.gupiao
collection = db.day

rows =  db.day.find({'symbol': 'SZ300033'})
timeArr = []


for row in rows:
    timeArr.append(row['time'])

rows2 =  db.day.find({'symbol': 'SZ300059'})
timeArr2 = []


for row in rows2:
    if row['time'] in timeArr:
        print 'true'
    else:
        print 'false'
