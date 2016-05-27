#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import tushare

client = MongoClient('localhost', 27017)
db = client.gupiao
collection = db.stock

data = {'symbol': 'aaa', 'name': 'bb'}
#collection.insert(data);

df = tushare.get_stock_basics()


for index, row in df.iterrows():
    code = '';
    if index[0] == '6':
        code = 'SH' + index
    else:
        code = 'SZ' + index
    #print code
    collection.insert({'code': code, 'name': row['name']});
