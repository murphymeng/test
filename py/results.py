#!/usr/bin/python
# -*- coding: utf-8 -*-

import falcon
import json
import time
import datetime
import requests
from pymongo import MongoClient
from account import Account
import random

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

        start_time = req.params['start_time']
        start_time_arr = map(int, start_time.split('-'))
        end_time = req.params['end_time']
        end_time_arr = map(int, end_time.split('-'))

        client = MongoClient('localhost', 27017)
        db = client.gupiao
        collection = db.day

        start_time = datetime.datetime(*start_time_arr)
        end_time = datetime.datetime(*end_time_arr)

        # 以上证指数为基准
        rows = db.day.find({
            'symbol': 'SH000001',
            'time': {'$gte': start_time, '$lt': end_time}
        })

        # 创建账户
        account = Account({})

        #最小持股天数
        minKeepDay = 2

        baseMoney = 10000 #起始资金
        preBaseData = None #前一天的基准数据
        preData = None #前一天数据
        baseResults = [] #基准数据结果集

        baseStock = 'SH000001'
        baseList = db.day.find({
            'symbol': baseStock,
            'time': {'$gte': start_time, '$lt': end_time}
        })
        baseDict = {}
        baseValue = None
        preSzzsData = None
        preDataList = None

        for row in baseList:
            if baseValue == None:
                baseValue = 10000.0 / row['open']
            baseDict[row['time']] = row['close'] * baseValue

        rowIndex = 0
        # 遍历上证指数
        for row in rows:
            rowIndex += 1
            # if row['time'] in baseDict and baseDict[row['time']]:
            #     baseResults.append({
            #         'time': str(row['time'])[0:10],
            #         'y': baseDict[row['time']]
            #     })
            # else:
            #     # 有待修改
            #     print '#######'
            #     baseResults.append({
            #         'time': str(row['time'])[0:10],
            #         'y': baseResults[-1][y]
            #     })
            #
            # if preBaseData:
            #     baseMoney = baseMoney * (row['close'] / preBaseData['close'])
            # preBaseData = row


            if account.hasStock == True:
                # 判断之前买入的股票今天是否有停牌，没有就卖出
                items = db.day.find({
                    'symbol': account.buyData['symbol'],
                    'time': row['time']
                })
                if (account.keepDays + 1) < minKeepDay or items.count() != 1:
                    account.keepStock(row['time'])
                else:
                    account.sell(items[0])
            elif preDataList and account.hasStock == False:
                #print preData
                buy_stock = None
                data = None
                result_data = None # 要买入的股票

                #tempArr = []
                for stock in preDataList:
                    #tempArr.append(stock);
                    items = db.day.find({
                        'symbol': stock['symbol'],
                        'time': row['time']
                    })
                    if items.count() == 1:
                        data = items[0]
                        if (float(data['open']) / stock['close'] - 1) * 100 > 9:
                            continue
                        else:
                            # 上市时间如果小于40天就过滤
                            gupiao = db.stock.find({'code': stock['symbol']})[0]
                            #print gupiao['name']
                            #print row['time']
                            age = (row['time'] - gupiao['start_time']).days
                            if age < 40:
                                continue
                            stock['total_value'] = gupiao['total_shares'] * stock['close']

                            if stock['total_value'] > 2000000:
                                continue

                            # print stock['total_value']
                            if (buy_stock and buy_stock['total_value'] < stock['total_value']) or buy_stock == None:
                                buy_stock = stock

                                # data是今天的数据, stock是昨天的数据
                                result_data = data
                                result_data['name'] = gupiao['name']
                    else:
                        continue


                # select_stock = random.choice(tempArr)
                # if select_stock:
                #     items = db.day.find({
                #         'symbol': select_stock['symbol'],
                #         'time': row['time']
                #     })
                #     gupiao = db.stock.find({'code': select_stock['symbol']})[0]
                #     # print 'item count:' + str(items.count())
                #     if items.count() == 1:
                #         result_data = items[0]
                #         result_data['name'] = gupiao['name']

                if result_data:
                    account.buy(result_data)
                else:
                    account.doNothing(row['time'])

            else:
                account.doNothing(row['time'])

            stocks = db.day.find({
                'percent': {'$gt': 8},
                #'macd': {'$gt': 0.21},
                'volume_rate': {'$gt': 4},
                'turnrate': {'$gt': 8},
                'time': row['time']
            })
            #print stocks.count()
            if stocks.count() > 0:
                preDataList = stocks
                # print 'rowindex:'
                # print rowIndex
                # print 'rows.count():'
                # print rows.count()
                # print ('rowIndex: ' + str(rowIndex))
                # print ('rows count: ' + str(rows.count()))
                if rowIndex == rows.count():
                    print 'last day'
                    for wantData in preDataList:
                        print wantData['symbol']
                #print preData
            else:
                preData = None
                preDataList = None

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

        if totalCount > 0:
            print '成功率' + str(float(winTime) / totalCount)


        res = {
            'baseStock': baseStock,
            'baseList': baseResults,
            'myList': account.historyList,
            'money': account.money
        }

        resp.body = json.dumps(res)


# 显示k线图
class Days(object):
    def on_get(self, req, resp):
        """Handles GET requests"""

        client = MongoClient('localhost', 27017)
        db = client.gupiao

        symbol = req.params['symbol']
        sell_time = req.params['sell_time']
        buy_time = req.params['buy_time']

        time_arr = sell_time.split('-')
        sell_time = datetime.datetime(int(time_arr[0]), int(time_arr[1]), int(time_arr[2]))
        start_time = sell_time - datetime.timedelta(days=30)
        end_time = sell_time + datetime.timedelta(days=30)

        rows = db.day.find({
            'symbol': symbol,
            'time': {'$gt': start_time, '$lt': end_time}
        })
        arr = []
        for row in rows:
            arr.append({
                'time': str(row['time'])[0:10],
                'open': row['open'],
                'close': row['close'],
                'high': row['high'],
                'low': row['low'],
                'percent': row['percent'],
                'turnrate': row['turnrate'],
                'volume': row['volume']
            })

        resp.body = json.dumps({
            'symbol': symbol,
            'arr': arr,
            'sellTime': req.params['sell_time'],
            'buyTime': req.params['buy_time']
        })



# falcon.API instances are callable WSGI apps
app = falcon.API(middleware=[CorsMiddleware()])

# Resources are represented by long-lived class instances
results = Results()

days = Days()

# things will handle all requests to the '/things' URL path
app.add_route('/results', results)

app.add_route('/days', days)
