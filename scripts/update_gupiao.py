#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import time
from pymongo import MongoClient
import tushare as ts

client = MongoClient('localhost', 27017)
db = client.gupiao

stockRows = db.stock.find()
arr2 = []
for stock in stockRows:
    arr2.append(stock['code'][2:])


df = ts.get_stock_basics()
temp = None

# for mf, row in df.iterrows():
#     print mf
arr = []
for index, row in df.iterrows():
    arr.append(str(index))



for index, row in df.iterrows():
    isNew = True

    for val2 in arr2:
        if str(val2) == str(index):
            isNew = False
            break

    if isNew == True:
        # pass
        stockCode = None
        start_time = None
        if index[0:1] == 6:
            stockCode = 'SH' + str(index)
        else:
            stockCode = 'SZ' + str(index)

        #print stockCode


        start_time = row['timeToMarket']
        start_time = str(start_time)
        #start_time = start_time.astype(str)
        start_time = time.strptime(start_time, "%Y%m%d")
        start_time = datetime.datetime(start_time.tm_year, start_time.tm_mon, start_time.tm_mday)

        data = {
            'code': stockCode,
            'name': row['name'],
            'float_shares': row['outstanding'],
            'total_shares': row['totals'],
            'start_time': start_time
        }

        db.stock.insert(data)
        #print data
        #db.day.insert(data)
        #print row['name']
