''' usage: from util import cache; then use cache.data (datacache object) '''
import os
import logging
import pickle
from datetime import timedelta, date
import pandas.io.data as pdata
import pandas as pd
import numpy as np
import scipy.stats as spstats
import scipy.optimize as scopt

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import DateFormatter
from matplotlib.dates import WeekdayLocator, MONDAY
import portfolio as pf

class DataCache(object):
    ''' mecanism to cache stock data if already downloaded '''
    datadir = os.path.dirname(os.path.realpath(__file__)) + '/../data'

    def __init__(self):
        self.cache = {}
        if not os.path.exists(self.datadir):
            os.makedirs(self.datadir)

    def DataReader(self, name, data_source="yahoo", start=None, end=None, lastn=None):
        ''' main access point '''
        if lastn:
             end = date.today()-timedelta(days=1)
             start = end-timedelta(days=lastn)
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

    def get_historical_closes(self, ticker, start_date=None, end_date=None):
        # get the data for the tickers.  This will be a panel
        p = self.DataReader(ticker, "yahoo", start=None, end=None)    
        # convert the panel to a DataFrame and selection only Adj Close
        # while making all index levels columns
        d = p.to_frame()['Adj Close'].reset_index()
        # rename the columns
        d.rename(columns={'minor': 'Ticker', 
                          'Adj Close': 'Close'}, inplace=True)
        # pivot each ticker to a column
        pivoted = d.pivot(index='Date', columns='Ticker')
        # and drop the one level on the columns
        pivoted.columns = pivoted.columns.droplevel(0)
        return pivoted


    def get_most_correlated(self, x, stocks=None, field='Adj Close', how='pct'):
        stocks = stocks if stocks else self.cache.keys()
        corr = self.get_correlation(stocks, field, how)
        data=corr[x].copy()
        data.sort(ascending=False)
        return data[1:]
            
    def get_data(self, stocks,  field='Adj Close', how=None):
        ''' get field for each stock in a single dataframe '''
	stocks = stocks if isinstance(stocks, list) else [stocks]
        data = pd.DataFrame({stocks[0]:self.DataReader(stocks[0])[field]})
        data = data.fillna(method='ffill')
        for stock in stocks[1:]:
            data = data.join(pd.DataFrame({stock:self.DataReader(stock)[field]}))
        if how=='pct':
            data = data.pct_change()
        elif how=='logdiff':
            data = np.log(data / data.shift(1)) 
        return data

    def plot(self, ticker, field='Adj Close'):
        data = self.DataReader(ticker)
        top = plt.subplot2grid((4,4), (0,0), rowspan=3, colspan=4)
        top.plot(data.index, data[field])
        plt.title('%s %s' %(ticker, field))
        plt.legend(loc=2)
        buttom = plt.subplot2grid((4,4), (3,0), rowspan=3, colspan=4)
        buttom.bar(data.index, data.Volume)
        plt.title('%s Volume' %(ticker))
        plt.gcf().set_size_inches(12, 8) 
        plt.subplots_adjust(hspace=0.75)

    def candle(self, ticker, field='Adj Close'):
        week_formatter = DateFormatter('%b %d')
        mondays = WeekdayLocator(MONDAY)
        data = self.DataReader(ticker)
        z = data.reset_index()
        fig, ax = plt.subplots()
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_major_formatter(week_formatter)
        z['date_num']=z['Date'].apply(lambda date: mdates.date2num(date.to_pydatetime()))
        subset = [tuple(x) for x in z[['date_num', 'Open', 'High', 'Low', 'Close']].values]
        candlestick_ohlc(ax, subset, width=0.6, colorup='g', colordown='r')

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

    def VaR(self, ticker='TSLA', precision=0.01, n=100, plot=False):
        z = spstats.norm.ppf(1-precision)
        data = self.DataReader(ticker)
        returns = pf.calc_daily_returns(data['Adj Close'])
        if plot:
            plt.hist(returns.values[1:], bins=100)
        position = n * data['Adj Close'][-1]
        VaR = position * (z * returns.std())
        print "VaR;",VaR," ","%.2f%%" %(VaR/position*100)

data = DataCache()

if __name__ == "__main__":
    #stocks = ["D-UN.TO", "USO", "OIL", "DBO", "OLO", "OLEM"]
    stocks = ["FAS","FAZ","MIDU","MIDZ","TNA","TZA","ERX","ERY","SPXL","SPXS","TECL","TECS","EDC","EDZ","DZK","DPK","DRN","DRV","MATL","BRZU","YINN","YANG","EURL","BAR","NUGT","DUST","CURE","INDL","JPNL","JNUG","JDST","LBJ","GASL","RETL","RUSL","RUSS","SOXL","SOXS","KORU","TYD","TYO","TMF","TMV","LBND","SBND","BUNT","JGBD","JGBT","TTT","UPRO","SPXU","FINU","FINZ","GDXX","GDXS","TQQQ","SQQQ","UDOW","SDOW","UMDD","SMDD","URTY","SRTY","UWTI","DWTI","UGLD","DGLD","UGAZ","DGAZ","USLV","DSLV"]
    #print 'pct change'
    #print data.get_correlation(stocks)
    #print 'logdiff'
    #print data.get_correlation(stocks, how='logdiff')
    print 'rolling'
    print data.get_rolling_corr('GLD', 'SPY', how='logdiff', plot=True)
    plt.show()
