#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
import requests
from pymongo import MongoClient
from account import Account

client = MongoClient('localhost', 27017)
db = client.gupiao
collection = db.day

start_time = datetime.datetime(2014, 4, 16)
end_time = datetime.datetime(2015, 4, 11)

rows = db.day.find({
    'symbol': 'SH000001',
    'time': {'$gt': start_time, '$lt': end_time}
})

account = Account({

})

preData = None
for row in rows:
    print row['time']
    if account.hasStock == True:
        items = db.day.find({
            'symbol': account.buyData['symbol'],
            'time': row['time']
        })
        print account.buyData['symbol']
        if items.count() >= 1:
            data = items[0]
            print str(row['time']) + ' ' + str(data['time'])
            account.sell(data)
        else:
            continue
    elif preData and account.hasStock == False:
        #print preData
        items = db.day.find({
            'symbol': preData['symbol'],
            'time': row['time']
        })
        #print '#'
        #print items.count()
        if items.count() == 1:
            data = items[0]
            if (float(data['open']) / preData['close'] - 1) * 100 < 9.8 and data['symbol'] != 'SZ000938':
                account.buy(data)


    stocks = db.day.find({
        'percent': {'$gt': 8},
        'macd': {'$gt': 0.21},
        'volume_rate': {'$gt': 3},
        'time': row['time']
    })
    if stocks.count() > 0:
        buy_stock = None
        #print row['time']
        for stock in stocks:
            gupiao = db.stock.find({'code': stock['symbol']})[0]
            stock['name'] = gupiao['name']
            #print '#' + stock['name']
            stock['total_value'] = gupiao['total_shares'] * stock['close']
            if (buy_stock and buy_stock['total_value'] > stock['total_value']) or buy_stock == None:
                buy_stock = stock
        #print buy_stock['name'] + ' ' + row['time'].strftime('%Y/%m/%d')
        preData = buy_stock
        #print preData
    else:
        preData = None

print account.money

#print r.text
