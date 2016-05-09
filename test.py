import numpy
import pandas
from pandas import DataFrame, Series

df = pandas.read_json('szzs.json')
money = 10000
for index, row in df.iterrows():
    #print row.open
    money = money * (row.close / row.open)
    print money

#print money
