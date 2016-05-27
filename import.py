#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.gupiao
collection = db.stock


session = requests.Session()
session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
session.get('https://xueqiu.com/')

for s in collection.find():
    time.sleep(2)
    code = s['code']
    r = session.get('https://xueqiu.com/stock/forchartk/stocklist.json?symbol='+ code + '&period=1day&type=before&end=1463365186825&_=1463365186825')
    print 'start parsing ' + code
    try:
        obj = r.json();
        chartlist = obj['chartlist']
        for data in chartlist:
            print data['time']
            #db.day.insert(data);
        print 'parse ' + code + ' successed'
    except:
        print 'parse ' + code + ' failed'
    break;




#print r.text
