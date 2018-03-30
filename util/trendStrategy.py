
from datetime import timedelta
from datetime import date
from strategy import Strategy 
from pandas.core.frame import DataFrame
import pandas as pd
from trendy import segtrends
import numpy as np
import csv
import sys
import logging
    

class TrendStrategy(Strategy):
    window = 21
    field = 'Close'
    predict = None

    def name(self):
        name = self.__class__.__name__
        if self.predict:
            return name+"_predicted"
        else:
            return name

    @classmethod
    def apply(cls, stock, data=None, writer=None):
        ''' return buy (1) or sale (-1) '''
        if not isinstance(data, DataFrame):
            start= date.today()-timedelta(days=cls.window)
            end = date.today()-timedelta(days=1)
            data = cls.datacache.DataReader(stock, "yahoo", start, end) 
        order = cls.get_order(data, segments=cls.window/5, writer=writer)
        return order

    @classmethod
    def get_order_features_from_trend(cls, segments, x_maxima, maxima, x_minima, minima):
        data = np.zeros((segments-1)*4)
        max_slop =  np.diff(maxima)/np.diff(x_maxima)
        min_slop =  np.diff(minima)/np.diff(x_minima)

        for i, el in enumerate((max_slop, min_slop)):
            start = i*(segments-1)
            data[start:start+segments-1]=el
        for i, el in enumerate((x_maxima, x_minima)):
            start = (i+2)*(segments-1)
            data[start:start+segments-1]=np.diff(el)

        return data

    @classmethod
    def get_order(cls, data, segments=2, window=7, writer=None, charts=False, verbose=False):
        ''' generate orders from segtrends '''
        price = data[cls.field]
        x_maxima, maxima, x_minima, minima = segtrends(price, segments, window, charts=charts)
        
        if writer or cls.predict:
            features = cls.get_order_features_from_trend(segments, x_maxima, maxima, 
                                                     x_minima, minima)
            vol_pct_change = data['Volume'][-(window+1):].pct_change()[-window:]
            last = data[cls.field][-1] 
            roll_mean_var = (pd.rolling_mean(data[cls.field][-window:], window)[-1]-last)/last
            roll_median_var = (pd.rolling_median(data[cls.field][-window:], window)[-1]-last)/last
            for add in (vol_pct_change, roll_mean_var, roll_median_var):
                features = np.append(features, add)
            if writer:
                writer.writerow(features)

        if cls.predict:
            order = -1 if cls.predict([features])==0 else 1
            return order
        else: 
            return cls.get_order_from_trend(minima, maxima, verbose)

    @classmethod
    def get_order_from_trend(cls, minima, maxima, verbose=False):
        # get 2 latest support point y values prior to x
        pmin = minima[-2:]
        pmax = maxima[-2:]
        # sell if support slop is negative
        min_sell = True if ((len(pmin)==2) and (pmin[1]-pmin[0])<0) else False 
        max_sell = True if ((len(pmax)==2) and (pmax[1]-pmax[0])<0) else False
        # if support down, sell
        if (min_sell and max_sell):
            buy = -1
        elif (not min_sell and not max_sell):
            buy = 1
        else: 
            buy = 0
    
        if verbose:
            print(min_sell, max_sell, buy)
    
        return buy

class OptTrendStrategy(TrendStrategy):
    @classmethod
    def get_order_from_trend(cls, minima, maxima, y, movy, last_buy):
        pmin = minima[-2:]
        pmax = maxima[-2:]
        # sell if support slop is negative
        min_sell = True if ((len(pmin)==2) and (pmin[1]-pmin[0])<0) else False 
        max_sell = True if ((len(pmax)==2) and (pmax[1]-pmax[0])<0) else False 
        
        # if support down, sell
        buy = -1 if (min_sell and max_sell) else 0
        # buy only if lower the moving average else sale
        buy = 1 if ((buy == 0) and (y<movy)) else -1
        # sell only if ...
        buy= -1 if ((buy == -1) and y>last_buy) else 1
        
        last_buy = y if (buy==1) else last_buy
        return buy, last_buy

    @classmethod
    def get_orders(cls, x, segments=2, window=7, charts=True, 
                   verbose=False):
        ''' generate orders from segtrends '''
        from filter import movingaverage
        from trendy import segtrends 
        x_maxima, maxima, x_minima, minima = segtrends(x, segments, window, charts)
        n = len(x)
        y = np.array(x)
        movy = movingaverage(y, window)
        
        # generate order strategy
        orders = np.zeros(n)
        last_buy = y[0]
        
        for i in range(1,n):
            # get 2 latest support point y values prior to x
            pmin = minima[np.where(x_minima<=i)]
            pmax = maxima[np.where(x_maxima<=i)]
            buy, last_buy = cls.get_order_from_trend(pmin, pmax, y[i], movy[i], last_buy)
            orders[i] = buy
        
        if verbose:
            print("orders", orders)
        return orders

    def simulate(self, stock, start, end=None, npoints=False,
                 charts=True, verbose=False, save=True):
        ''' start is a datetime or nb days prior to now '''
        logging.info(sys._getframe().f_code.co_name)
        data = self.get_data(stock, start, end, npoints, verbose=verbose)
        n = len(data)
        if verbose:
            print("period:", data.index[0], data.index[-1], ";ndays =",n)
            print(data['Open'])
        #TODO: check open
        orders = self.get_orders(data['Open'], segments=n/5, window=7, charts=charts)
        
        return orders, data 
