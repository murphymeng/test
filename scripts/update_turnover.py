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

    df = ts.get_hist_data(symbol[2:])

    for index, row in df.iterrows():

        index_arr = index.split('-');

        index_datetime = datetime.datetime(int(index_arr[0]), int(index_arr[1]), int(index_arr[2]))

        db.day.find_one_and_update({'symbol': symbol, 'time': index_datetime, 'turnover': {'$exists': False}}, {'$set': {'turnover': row['turnover']}})

    print symbol + ' done'
