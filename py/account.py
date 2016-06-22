#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.gupiao

class Account:


    def __init__(self, opts):
        for key, value in opts.iteritems():
            self.key = value
        self.name = ''
        self.money = 10000
        self.originMoney = 1
        self.hasStock = False
        self.keepDays = 0
        self.singleProfit = 1
        self.moneyArr = [1]
        self.historyList = []
        self.profitList = []

    def buy(self, data, preData = None):
        self.hasStock = True
        self.buyData = data
        self.keepDays += 1

        # 扣除佣金
        self.money = (1 - 0.0003) * self.money

    def sell(self, data):
        singleProfit = 1
        if float(data['high']) / self.buyData['close'] >= 1.09:
            singleProfit = self.buyData['close'] / self.buyData['open'] * 1.09
            #print singleProfit
        else:
            singleProfit = data['close'] / self.buyData['open']

        self.profitList.append(singleProfit)

        #singleProfit = data['close'] / self.buyData['open']

        self.money = float(self.money) * singleProfit

        # if singleProfit < 1:
        #     print data[u'symbol'] + ' ' + str(data['time'])
        #     print db.stock.find({'code': data[u'symbol']})[0]['name']
        #     print '买入日期：' + str(self.buyData['time'])
        #     print '卖出日期：' + str(data['time'])
        #     print '单次收益：' + str( (singleProfit - 1) * 100 ) + '%'
        #     print "\n"
        self.moneyArr.append(self.money)
        if data[u'symbol']:

            self.historyList.append({
                'name': self.buyData[u'name'],
                'symbol': data[u'symbol'],
                'profit': str(round(100 * (singleProfit - 1), 2)) + '%',
                'buyTime': str(self.buyData['time'])[0:10],
                'sellTime': str(data['time'])[0:10],
                'money': self.money,
                'time': str(data['time'])[0:10]
            })
        #print self.moneyArr
        self.hasStock = False
        self.reset()

        # 扣除佣金和印花税
        self.money = (1 - 0.0013) * self.money

    def doNothing(self, time):
        a = 1
        # self.historyList.append({
        #     'time': str(time)[0:10],
        #     'money': self.money
        # })

    def keepStock(self, time):
        # self.historyList.append({
        #     'time': str(time)[0:10],
        #     'money': self.money
        # })
        self.keepDays += 1

    def reset(self):
        self.keepDays = 0
        self.singleProfit = 1
