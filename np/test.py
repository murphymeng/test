import pandas as pd
import numpy as np

def test(t, a=1, b=2):
    print 't:' + str(t)
    print 'a:' + str(a)
    print 'b:' + str(b)

#print pd.date_range('20160101', periods=6)

df = pd.DataFrame(np.random.randn(3,4), index=pd.date_range('20160101', periods=3), columns = list('abcd'))


df2 = pd.DataFrame({ 'A' : 1.,
                     'B' : pd.Timestamp('20130102'),
                     'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
                     'D' : np.array([3] * 4,dtype='int32'),
                     'E' : pd.Categorical(["test","train","test","train"]),
                     'F' : 'foo' })


df['e'] = np.nan
df.fillna(value=5)

print df
