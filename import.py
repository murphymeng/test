#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.gupiao
collection = db.stock


session = requests.Session()
session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
session.get('https://xueqiu.com/')

start_time = datetime.datetime(2005, 1, 1)

for s in collection.find({'done': False}):
    #time.sleep(2)
    code = s['code']
    r = session.get('https://xueqiu.com/stock/forchartk/stocklist.json?symbol='+ code + '&period=1day&type=before&end=1463365186825&_=1463365186825')
    print 'start parsing ' + code
    try:
        obj = r.json();
        chartlist = obj['chartlist']
        for data in chartlist:
            day_time = data['time'][0:11] + data['time'][-4:]
            day_time = time.strptime(day_time, "%a %b %d %Y")
            day_time = datetime.datetime(day_time.tm_year, day_time.tm_mon, day_time.tm_mday)
            data['time'] = day_time
            data['symbol'] = code
            if day_time > start_time:
                db.day.insert(data);
        print 'parse ' + code + ' successed'
        db.stock.find_one_and_update({'code': code}, {'$set': {'done': True}})
    except:
        print 'parse ' + code + ' failed'




#print r.text
