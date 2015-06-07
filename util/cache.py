''' usage: from util import cache; then use cache.data (datacache object) '''
import os
import logging
import pickle
import pandas.io.data as pdata
import pandas as pd
import numpy as np

class DataCache(object):

    datadir = os.path.dirname(os.path.realpath(__file__)) + '/../data'

    def __init__(self):
        self.cache = {}

    def DataReader(self, name, data_source="yahoo", start=None, end=None):
        datafilepath = self.datadir + '/' + name + '.p'
        def get_date_range(start,end):
            start = start if start is not None else self.cache[name].index[0]
            end = end if end is not None else self.cache[name].index[-1]
            return self.cache[name][start:end]

        if name in self.cache:
	    logging.info('Retreiving ' + name + ' from cache')
            return get_date_range(start, end)
        elif os.path.isfile(datafilepath):
            self.cache[name] = pickle.load(open(datafilepath, "rb"))
	    logging.info('Retreiving ' + name + ' from file')
            return get_date_range(start, end)
        else:
            data = pdata.DataReader(name, data_source)
            self.cache[name] = data
            pickle.dump(data, open(datafilepath,"wb"))
	    logging.info('Retreiving ' + name + ' from internet and stored')
            return get_date_range(start, end)

    def get_most_correlated(self, x, stocks=None, field='Adj Close'):
        stocks = stocks if stocks else self.cache.keys()
        corr = self.get_correlation(stocks, field)
        data=corr[x].copy()
        data.sort(ascending=False)
        return data[1:]
            
    def get_correlation(self, stocks, field='Adj Close'):
        ''' get correlation matrix or best correlation list of 'get_best_of' '''

        data = pd.DataFrame({stocks[0]:self.DataReader(stocks[0])[field].pct_change()})
        for stock in stocks[1:]:
            data = data.join(pd.DataFrame({stock:self.DataReader(stock)[field].pct_change()}))

        return data.corr()

    def get_rolling_corr(self, a, b, window=252, field='Adj Close', plot=True):
        data = pd.DataFrame({a:self.DataReader(a)[field].pct_change()})
        data = data.join(pd.DataFrame({b:self.DataReader(b)[field].pct_change()}))
        corr = pd.rolling_corr(rets[a], rets[b], window)
        if plot:
            corr.plot(grid=True, style='b')
        return corr

data = DataCache()

if __name__ == "__main__":
    print data.DataReader('TSLA')
    stocks = ["TSLA", "GS", "SCTY", "AMZN", "CSCO",'FB',
              'UTX','JCI',"GOOGL",'BP','MSFT', 'IBM','NUAN','YHOO']
    print data.get_correlation(stocks)
    print data.get_most_correlated('SCTY', stocks)
