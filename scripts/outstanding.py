#!/usr/bin/python
# -*- coding: utf-8 -*-
import tushare as ts
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.gupiao

df = ts.get_stock_basics()

for s in db.stock.find({}):
    code = s['code']

    #print ts.get_stock_basics().loc[s['code'][2:]]
    #流通股本
    #float_shares = ts.get_stock_basics().loc[s['code'][2:]].outstanding
    #db.stock.find_one_and_update({'code': code}, {'$set': {'float_shares': float_shares}})

    total_shares = df.loc[s['code'][2:]].totals
    db.stock.find_one_and_update({'code': code}, {'$set': {'total_shares': total_shares}})
    print str(s['code']) + ' updated'
