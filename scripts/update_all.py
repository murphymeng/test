#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import time
from pymongo import MongoClient
import tushare as ts

client = MongoClient('localhost', 27017)
db = client.gupiao


stockRows = db.stock.find()

basicInfos = ts.get_stock_basics()

for stock in stockRows:
    symbol = stock['code']

    if symbol == 'SH000001':
        continue


    rows = db.day.find({
        'symbol': symbol
    }).sort('time', -1).limit(1)

    for row in rows:
        start_time = str(row['time'])[0:10]
        #end_time = str(datetime.datetime.now())[0:10]

    df = ts.get_hist_data(symbol[2:],start=start_time)
    df = df.sort_index(ascending=True)

    for index, row in df.iterrows():

        index_arr = index.split('-')

        index_datetime = datetime.datetime(int(index_arr[0]), int(index_arr[1]), int(index_arr[2]))
        #print index_datetime

        findOne = db.day.find_one({
            'symbol': symbol,
            'time': index_datetime
        })

        if findOne == None:
            gupiao = basicInfos.loc[symbol[2:]]

            #print gupiao['totals']
            #print (row['volume'] / gupiao['totals']) * 100
            data = {
                'high': row['high'],
                'low': row['low'],
                'open': row['open'],
                'close': row['close'],
                'symbol': symbol,
                'ma5': row['ma5'],
                'ma10': row['ma10'],
                'ma20': row['ma20'],
                'chg': row['price_change'],
                'time': index_datetime,
                'percent': row['p_change'],
                'volume': row['volume'] * 100,
                'turnrate': (row['volume'] / gupiao['totals'] ),
                'turnover': row['turnover']
            }
            #print data
            db.day.insert(data)
            #break;
    print symbol + ' done'
