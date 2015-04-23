import numpy as np
import pandas as pd
from filter import movingaverage
import math

import pandas.io.data as pdata
from datetime import timedelta
from datetime import date
from visu import plot_orders
#!pip install mlboost
from mlboost.core.pphisto import SortHistogram

# little hack to make in working inside heroku submodule
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

log_momentum = lambda previous: round(math.log(1+2*abs(previous))+1)
double_momentum = lambda previous: 2*abs(previous)
exp_momentum = lambda previous: round(math.pow(abs(previous), 2))
no_momentum = lambda previous:round(abs(previous))

import abc

class Strategy(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def apply(self, stock, data=None):
        """ return buy(1) or sell(-1) """
        return

    @classmethod
    def simulate(cls, stock, start, end=None, verbose=True, charts=True):
        ''' start is a datetime or nb days prior to now '''
        end = end if end!=None else date.today()-timedelta(days=1)
        if isinstance(start, int):
            start = end-timedelta(days=start)
        # add required padding 
        data = pdata.DataReader(stock, "yahoo", 
                                start=start-timedelta(days=cls.window),
                                end=end)
        n = len(data)
        orders=np.zeros(n)
        for i in range(n):
            start_i = start+timedelta(days=-cls.window+i)
            end_i = start+timedelta(days=i)
            data_i = data[start_i:end_i]
            order = cls.apply(stock, data_i)
            orders[i]=order
            if verbose:
                print end_i+timedelta(days=1), order
        
        if charts:
            p = data[cls.field][-n:]
            plot_orders(p, orders, stock)
            
        return orders, data

from trendStrategy import TrendStrategy

class Eval:
    momentum = log_momentum
    ''' construct a strategy evaluator '''
    def __init__(self, field='Close', months=12, 
                 init_cash=20000, init_shares=30, min_trade=30, 
                 min_shares=0, min_cash=0, trans_fees=10, 
                 verbose=False, debug=False):
        ''' min trade is either or % in initial_cash or a number of shares '''
        self.field=field
        self.months=months
        self.init_cash = init_cash
        self.init_shares = init_shares
        self.min_trade = min_trade #if isinstance(min_trade, int) else int(min_trade*init_cash)
        self.min_shares = min_shares
        self.min_cash = min_cash
        self.trans_fees = trans_fees
        self.verbose = verbose
        self.debug = debug

    def set_momentums(cls, buy='log', sell='log'):
        def get(name):
            if name == 'log':
                return log_momentum
            elif name=='double':
                return double_momentum
            elif name == 'exp':
                return exp_momentum
            else:
                return no_momentum
        cls.buy_momentum = get(buy)
        cls.sell_momentum = get(sell)
                    
    def run(self, stockname, strategy='trends', signalType='shares', 
            save=False, charts=True):
        ''' run the evaluation '''

        self.stockname = stockname
        if self.verbose:
            print "Evaluation ", self.stockname
    
        # get data
        n = int((5*4)*self.months)
                
        # apply the strategy
        if strategy == 'trends':
            title = 'automatic strategy base %s' %stockname
            self.orders, self.data = TrendStrategy.simulate(stockname, n)
            n = len(self.orders)
            price = self.data[self.field]
            self.BackTest(self.orders)
            plot_orders(price, self.data['trade'], stockname, show=True)
            #print self.data.ix[:,['shares', 'cash', 'trade', 'Adj Close', 'value', 'pnl']]
            return self.data

        elif strategy == 'old':
            self.data = pdata.DataReader(self.stockname, "yahoo")
            price = self.data[self.field][-n:] 
        
            orders = self.orders_from_trends(price, segments=n/5, 
                                             charts=(charts and self.debug), 
                                             buy_momentum=self.buy_momentum,
                                             sell_momentum=self.sell_momentum,
                                             title='title');
            signal = self.orders2strategy(orders, price[-n:], self.min_trade)
            
            # run the backtest
            import lib.backtest as bt
            self.backtest = bt.Backtest(price, signal, signalType=signalType,
                                        initialCash=self.init_cash, initialShares=self.init_shares,
                                        min_cash=self.min_cash, min_shares=self.min_shares,
                                        trans_fees=self.trans_fees)
        
            if True:
                self.visu(save)

            return self.backtest.data
        else:
            raise("unknown strategy '%s'" %strategy)
        

    def BackTest(self, orders, buy_field='High', sell_field='Low', verbose=False):
        ''' price field = Open, High, Low, Close, Adj Close ''' 
        n = len(orders)
        cash = self.init_cash
        shares = self.init_shares
        fees=0
        self.shares = np.zeros(n)
        self.cash = np.zeros(n)
        self.trades = np.zeros(n)
        self.fees = np.zeros(n)

        def momentum(orders, i):
            order = orders[i]
            if i>1:
                if order==orders[i-1]:
                    if order>0:
                        orders[i] = self.buy_momentum(orders[i-1])
                    elif order<0:
                        orders[i] = self.sell_momentum(orders[i-1])
            return orders[i]

        if verbose:
            print "#\tcash\ttrade\tshares\tprice\tvalue"
            price = self.data['Adj Close'][0]
            value = cash+price*shares
            print "\t".join([str(el) for el in (0, cash, 0, shares, price, value)])
                        
        for i in range(len(orders)):
            order = momentum(orders, i)
            trade = (order*self.min_trade)
            trade_value = 0
            if order!=0:
                fees+=self.trans_fees
            # if buy
            if order>0:
                buy_price = self.data[buy_field][i]
                trade_value = trade*buy_price + self.trans_fees
                if trade_value > cash:
                    trade = int((cash-self.trans_fees)/buy_price)
                    trade_value = trade*buy_price + self.trans_fees
            elif order<0: #sell 
                if trade>shares:
                    trade = -shares
                sell_price = self.data[sell_field][i]
                trade_value = trade*sell_price + self.trans_fees
            # update shares
            shares += trade
            cash -= trade_value
            self.trades[i] = trade
            self.shares[i] = shares
            self.cash[i] = cash
            self.fees[i] = fees
            if verbose:
                price = self.data['Adj Close'][i]
                value = cash+price*shares
                print "\t".join([str(el) for el in (i+1, cash, trade, shares, price, value)])

        # create missing fields
        self.data['shares'] = self.shares
        self.data['cash'] = self.cash
        self.data['trade'] = self.trades
        self.data['fees'] = self.fees
        self.data['value'] = self.data['shares'] * self.data['Adj Close']
        self.data['total'] = self.data['cash']+self.data['value']
        self.data['pnl'] = self.data['total'].diff()

    def visu(self, save=False):
        from pylab import title, figure, savefig, subplot, show
        print "#1) Automatic buy/sales visualisation of the current strategy (buy=long, short=sale)"
        if save:
            subplot(211)
        else:
            figure()
        self.backtest.plotTrades(self.stockname)
        print "#2) Evaluation of the strategy (PnL (Profit & Log) = Value today - Value yesterday)"
        if save:
            subplot(212)
        else:
            figure()
        self.backtest.pnl.plot()
        title('pnl '+self.stockname)
        if save:
            savefig('eval.png')
        
        print "#3) big picture: Price, shares, value, cash & PnL"
        self.backtest.data.plot()
        title('all strategy data %s' %self.stockname)
        if save:
            savefig('all.png')
        else:
            show()

    @classmethod
    def orders2strategy(cls, orders, price, min_stocks=1):
        strategy = pd.Series(index=price.index) 
        orders=[el*min_stocks for el in orders]
        # create a stratgy from order
        for i, idx in enumerate(price.index):
            if orders[i]!=0:
                strategy[idx] = orders[i]
        return strategy

    @classmethod
    def orders_from_trends(cls, x, segments=2, charts=True, window=7, 
                           sell_momentum=no_momentum, 
                           buy_momentum=no_momentum,
                           title=None):
        ''' generate orders from segtrends '''
        x_maxima, maxima, x_minima, minima = segtrends(x, segments, charts, window, title)
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
            # sell only if ... # MUCH BETTER WITHOUT IT
            #buy= -1 if ((buy == -1) and y[i]>last_buy) else 1
      
            buy_price_dec = y[i]<last_buy
            sale_price_dec = y[i]<last_sale
            orders[i] = buy
            last_buy = y[i] if (buy==1) else last_buy
            last_sale = y[i] if (buy==-1) else last_sale
        
            
            # add momentum for buy 
            if buy_momentum and (buy==1) and (orders[i-1]>=1):
                #if buy_price_dec:
                #orders[i]=orders[i-1]*2#round(math.log(2*orders[i-1])+1)
                orders[i]=buy_momentum(orders[i-1])#round(math.log(2*orders[i-1])+1)
                #else:
                #   orders[i]=max(1, round(orders[i-1]/2))
                # add momentum for sale
            elif sell_momentum and (buy==-1) and (orders[i-1]<=-1):
                #if sale_price_dec:
                #orders[i]*=round(math.log(abs(orders[i-1]*2))+1)
                orders[i]=-sell_momentum(orders[i-1])
                #else:
                #    orders[i]=max(1, round(orders[i-1]/2))
        
        # ensure no order are taken at the begining
        for i in range(window):
            orders[i]=0
        return orders
    
    def eval_best(self, stocks=["TSLA", "GS", "SCTY", "AMZN", "CSCO", 'UTX','JCI',"GOOGL",'AAPL','BP','MSFT'],  charts=False):
        # try current strategy on different stock
        trademap = {}
        tradedetails = {}

        for i, stock in enumerate(stocks):
            trade = self.run(stock, charts=charts)
            if False:
                print i, stock, trade.ix[-1:,'cash':]
            trademap[stock] = trade[-1:]['pnl'][-1]
            tradedetails[stock] = trade[-1:]
        
        st = SortHistogram(trademap, False, True)
        
        print "Here are the Stocks sorted by PnL"
        for i,el in enumerate(st):
            stock, value = el
            print "#", i+1, stock
            print tradedetails[stock]
        return st

if __name__ == "__main__":
    #eval(charts=True)
    print Strategy.apply('TSLA')
    print Strategy.simulate('TSLA', 300)
    pass
