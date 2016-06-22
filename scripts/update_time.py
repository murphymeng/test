#!/usr/bin/python
# -*- coding: utf-8 -*-
# 更新上市日期
import tushare as ts
import time
import numpy as np
import datetime
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.gupiao

df = ts.get_stock_basics()

for s in db.stock.find({}):
    code = s['code']

    start_time = df.loc[s['code'][2:]].timeToMarket
    satrt_time = str(start_time)
    #start_time = satrt_time[0:3] + ' ' + start_time[4:5] + ' ' + start_time[6:7]
    start_time = start_time.astype(str)
    #print type(start_time.astype(str))
    #print start_time[0:4] + ' ' + start_time[4:6] + ' ' + start_time[6:8]
    #break

    start_time = time.strptime(start_time, "%Y%m%d")
    start_time = datetime.datetime(start_time.tm_year, start_time.tm_mon, start_time.tm_mday)

    db.stock.find_one_and_update({'code': code}, {'$set': {'start_time': start_time}})
