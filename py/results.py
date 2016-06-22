#!/usr/bin/python
# -*- coding: utf-8 -*-

import falcon
import json
import time
import datetime
import requests
from pymongo import MongoClient
from account import Account

ALLOWED_ORIGINS = ['http://localhost']

class CorsMiddleware(object):

    def process_request(self, request, response):
        origin = request.get_header('Origin')
        if origin in ALLOWED_ORIGINS:
            response.set_header('Access-Control-Allow-Origin', origin)


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class Results(object):
    def on_get(self, req, resp):
        """Handles GET requests"""

        client = MongoClient('localhost', 27017)
        db = client.gupiao
        collection = db.day

        start_time = datetime.datetime(2015, 10, 19)
        end_time = datetime.datetime(2016, 4, 11)

        rows = db.day.find({
            'symbol': 'SH000001',
            'time': {'$gt': start_time, '$lt': end_time}
        })

        account = Account({

        })

        #最小持股天数
        minKeepDay = 2

        baseMoney = 10000
        preBaseData = None
        preData = None
        baseResults = []

        baseStock = 'SH000001'
        baseList = db.day.find({
            'symbol': baseStock,
            'time': {'$gt': start_time, '$lt': end_time}
        })
        baseDict = {}
        baseValue = None
        preSzzsData = None

        for row in baseList:
            if baseValue == None:
                baseValue = float(10000) / row['open']
            baseDict[row['time']] = row['close'] * baseValue

        for row in rows:
            if row['time'] in baseDict and baseDict[row['time']]:
                baseResults.append({
                    'time': str(row['time'])[0:10],
                    'y': baseDict[row['time']]
                })
            else:
                print 'bb'
                baseResults.append({
                    'time': str(row['time'])[0:10],
                    'y': baseResults[-1][y]
                })

            if preBaseData:
                baseMoney = baseMoney * (row['close'] / preBaseData['close'])


            preBaseData = row
            if account.hasStock == True:
                # 判断之前买入的股票今天是否有停牌，没有就卖出
                items = db.day.find({
                    'symbol': account.buyData['symbol'],
                    'time': row['time']
                })
                if (account.keepDays + 1) < minKeepDay or items.count() != 1:
                    account.keepStock(row['time'])
                else:
                    data = items[0]
                    account.sell(data)
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
                    data['name'] = preData['name']


                    if (float(data['open']) / preData['close'] - 1) * 100 < 6.7 and data['symbol'] != 'SZ000938':
                         account.buy(data)
                account.doNothing(row['time'])
            else:
                account.doNothing(row['time'])


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

                    # 上市时间如果小于40天就过滤
                    age = (row['time'] - gupiao['start_time']).days
                    if age < 40:
                        continue

                    # 如果昨天涨幅也很高则过滤


                    #print '#' + stock['name']
                    stock['total_value'] = gupiao['total_shares'] * stock['close']
                    if (buy_stock and buy_stock['total_value'] > stock['total_value']) or buy_stock == None:
                        buy_stock = stock
                #print buy_stock['name'] + ' ' + row['time'].strftime('%Y/%m/%d')
                preData = buy_stock
                #print preData
            else:
                preData = None

            preSzzsData = row

        print len(account.historyList)
        print len(baseResults)
        print rows.count()

        totalCount = 0
        winTime = 0

        for profit in account.profitList:
            totalCount += 1
            #print profit
            if profit > 1:
                winTime += 1
        print '成功率' + str(float(winTime) / totalCount)


        res = {
            'baseStock': baseStock,
            'baseList': baseResults,
            'myList': account.historyList,
            'money': account.money
        }

        resp.body = json.dumps(res)

# falcon.API instances are callable WSGI apps
app = falcon.API(middleware=[CorsMiddleware()])

# Resources are represented by long-lived class instances
results = Results()

# things will handle all requests to the '/things' URL path
app.add_route('/results', results)
