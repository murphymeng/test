#!/usr/bin/python
# -*- coding: utf-8 -*-
import tushare as ts
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.gupiao

lastStock = None;

for stock in db.day.find({}):
    if lastStock and stock['volume'] and lastStock['volume'] and (stock['symbol'] == lastStock['symbol']):
        volume_rate = float(stock['volume']) / lastStock['volume']
        volume_rate = round(volume_rate, 2)
        db.day.find_one_and_update({'_id': ObjectId(stock['_id'])}, {'$set': {'volume_rate': volume_rate}})
    lastStock = stock
