#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import time
from bson.objectid import ObjectId
from pymongo import MongoClient
import tushare as ts

client = MongoClient('localhost', 27017)
db = client.gupiao


stockRows = db.stock.find()

basicInfos = ts.get_stock_basics()

for stock in stockRows:

    symbol = stock['code']

    rows = db.day.find({
        'symbol': symbol,
        'time': {
            '$gt': datetime.datetime(2016, 6, 30)
        }
    }).sort('time', 1)

    preRow = None

    for row in rows:
        if 'volume_rate' not in row and preRow:
            volume_rate = float(row['volume']) / preRow['volume']
            volume_rate = round(volume_rate, 2)
            #print volume_rate
            db.day.find_one_and_update({'_id': ObjectId(row['_id'])}, {'$set': {'volume_rate': volume_rate}})

        preRow = row
