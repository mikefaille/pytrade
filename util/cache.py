''' usage: from util import cache; then use cache.data (datacache object) '''
import os
import logging
import pickle
import pandas.io.data as pdata
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DataCache(object):

    datadir = os.path.dirname(os.path.realpath(__file__)) + '/../data'

    def __init__(self):
        self.cache = {}

    def DataReader(self, name, data_source="yahoo", start=None, end=None):
        name = name.lower()
        datafilepath = self.datadir + '/' + name + '.p'
        def get_date_range(start, end):
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

    def get_most_correlated(self, x, stocks=None, field='Adj Close', how='pct'):
        stocks = stocks if stocks else self.cache.keys()
        corr = self.get_correlation(stocks, field, how)
        data=corr[x].copy()
        data.sort(ascending=False)
        return data[1:]
            
    def get_data(self, stocks,  field='Adj Close', how=None):
        ''' get field for each stock in a single dataframe '''
        data = pd.DataFrame({stocks[0]:self.DataReader(stocks[0])[field]})
        data = data.fillna(method='ffill')
        for stock in stocks[1:]:
            data = data.join(pd.DataFrame({stock:self.DataReader(stock)[field]}))
        if how=='pct':
            data = data.pct_change()
        elif how=='logdiff':
            data = np.log(data / data.shift(1)) 
        return data

    def get_correlation(self, stocks, field='Adj Close', how='pct'):
        ''' get correlation matrix or best correlation list of 'get_best_of' '''
        data = self.get_data(stocks, field, how)
        return data.corr()

    def show_correlation(self, a, b, field='Adj Close', how='pct'):
        data = self.get_data([a, b], field, how)
        model = pd.ols(y=data[a], x=data[b])
        plt.plot(data[a], data[b], 'r.')
        ax = plt.axis()  # grab axis values
        x = np.linspace(ax[0], ax[1] + 0.01)
        plt.plot(x, model.beta[1] + model.beta[0] * x, 'b', lw=2)
        plt.grid(True)
        plt.axis('tight')
        plt.xlabel(a)
        plt.ylabel(b)

    def get_rolling_corr(self, a, b, window=252, field='Adj Close', how='pct', 
                         plot=True):
        data = self.get_data([a, b], field, how)
        corr = pd.rolling_corr(data[a], data[b], window)
        if plot:
            corr.plot(grid=True, style='b')
            data.plot()
        return corr

data = DataCache()

if __name__ == "__main__":
    print data.DataReader('TSLA')
    stocks = ["TSLA", "GS", "SCTY", "AMZN", "CSCO",'FB',
              'UTX','JCI',"GOOGL",'BP','MSFT', 'IBM','NUAN','YHOO']
    print data.get_correlation(stocks)
    print data.get_most_correlated('SCTY', stocks)
