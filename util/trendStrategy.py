
from datetime import timedelta
from datetime import date
from strategy import Strategy 
from pandas.core.frame import DataFrame
from trendy import segtrends
import numpy as np

class TrendStrategy(Strategy):
    window = 21
    field = 'Close'
    
    @classmethod
    def apply(cls, stock, data=None, writer=None):
        ''' return buy (1) or sale (-1) '''
        if not isinstance(data, DataFrame):
            start= date.today()-timedelta(days=cls.window)
            end = date.today()-timedelta(days=1)
            data = cls.datacache.DataReader(stock, "yahoo", start, end) 
        price = data[cls.field]
        order = cls.trend_order(price, segments=cls.window/5, writer=writer)
        return order

    @classmethod
    def trend_order(cls, y, segments=2, window=7, writer=None, charts=False, verbose=False):
        ''' generate orders from segtrends '''
        x_maxima, maxima, x_minima, minima = segtrends(y, segments, window, charts=charts)
        if writer:
            data = np.zeros((segments-1)*4)
            for i, el in enumerate((x_maxima, maxima, x_minima, minima)):
                start = i*(segments-1)
                data[start:start+segments-1]=np.diff(el)
            writer.writerow(data)
        
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
            print min_sell, max_sell, buy
    
        return buy
