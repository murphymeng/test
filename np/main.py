#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import pandas.io.data as web
# import matplotlib
# import matplotlib.pyplot as plt
import datetime
import tushare as ts

start = datetime.datetime(2013, 1, 1)

end = datetime.datetime(2013, 2, 3)

f = web.DataReader("F", 'yahoo', start, end)

f['daily_return'] = f.Close / f.Close.shift(1)

# f['daily_return2'] = (f[1:] / f[:-1].Close) - 1

f2 = f.fillna(method='bfill')

print f2



#f2.plot(y='daily_return')


# plt.show()
#print f.Close.shift(1)


#
# df = ts.get_stock_basics()
#
# print df
