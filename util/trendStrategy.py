
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
        order = cls.get_order(price, segments=cls.window/5, writer=writer)
        return order

    @classmethod
    def get_order(cls, y, segments=2, window=7, writer=None, charts=False, verbose=False):
        ''' generate orders from segtrends '''
        x_maxima, maxima, x_minima, minima = segtrends(y, segments, window, charts=charts)
        max_slop =  np.diff(maxima)/np.diff(x_maxima)
        min_slop =  np.diff(minima)/np.diff(x_minima)
        if writer:
            data = np.zeros((segments-1)*4)
            for i, el in enumerate((max_slop, min_slop)):
                start = i*(segments-1)
                data[start:start+segments-1]=el
            for i, el in enumerate((x_maxima, x_minima)):
                start = (i+2)*(segments-1)
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

class OptTrendStrategy(TrendStrategy):
    
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
        last_sale = y[0]
        
        for i in range(1,n):
            # get 2 latest support point y values prior to x
            pmin = list(minima[np.where(x_minima<=i)][-2:])
            pmax = list(maxima[np.where(x_maxima<=i)][-2:])
            # sell if support slop is negative
            min_sell = True if ((len(pmin)==2) and (pmin[1]-pmin[0])<0) else False 
            max_sell = True if ((len(pmax)==2) and (pmax[1]-pmax[0])<0) else False 
            
            # if support down, sell
            buy = -1 if (min_sell and max_sell) else 0
            # buy only if lower the moving average else sale
            buy = 1 if ((buy == 0) and (y[i]<movy[i])) else -1
            # sell only if ...
            buy= -1 if ((buy == -1) and y[i]>last_buy) else 1
            
            buy_price_dec = y[i]<last_buy
            sale_price_dec = y[i]<last_sale
            orders[i] = buy
            last_buy = y[i] if (buy==1) else last_buy
            last_sale = y[i] if (buy==-1) else last_sale
        
        # OUTPUT
        if verbose:
            print "orders", orders
        return orders

    @classmethod
    def simulate(cls, stock, start, end=None, npoints=False,
                 charts=True, verbose=False, save=True):
        ''' start is a datetime or nb days prior to now '''
        data = cls.get_data(stock, start, end, npoints, verbose=verbose)
        n = len(data)
        if verbose:
            print "period:", data.index[0], data.index[-1], ";ndays =",n
            print data['Open']
        orders = cls.get_orders(data['Open'], segments=n/5, window=7, charts=charts)
        if save:
            with open('%s_trade.csv' %stock, 'wb') as f:
                writer = csv.writer(f)
                #writer.writerow(['date', 'order'])
                for date, order in zip(data.index[cls.window:], orders[cls.window:]):
                    writer.writerow([date, order])
        return orders, data 
