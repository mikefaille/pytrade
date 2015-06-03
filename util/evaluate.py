import numpy as np
import pandas as pd
from filter import movingaverage
import math
import logging
import pandas as pd
from util.cache import DataCache
from datetime import timedelta
from datetime import date
from visu import plot_orders, plot_field
#!pip install mlboost
from mlboost.core.pphisto import SortHistogram

from sys import maxint as MAXINT

# little hack to make in working inside heroku submodule
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

log_momentum = lambda previous: round(math.log(1+2*abs(previous))+1)
double_momentum = lambda previous: 2*abs(previous)
exp_momentum = lambda previous: round(math.pow(abs(previous+.5), 2))
no_momentum = lambda previous:abs(previous )

from strategy import Strategy
# import strategies 
from trendStrategy import TrendStrategy, OptTrendStrategy

def get_strategy(name):
    if name=="trend":
        return TrendStrategy()
    elif name=="opt_trend":
        return OptTrendStrategy()
    else:
        logging.warning("unknown strategy %s" %name)
        return name

pd.set_option('precision', 3) 
pd.set_option('colheader_justify' ,'left')
pd.set_option('expand_frame_repr' , False)
header = ['cash', 'shares', 'value', 'trade', 'fees', 'Open', 'total', 'pnl']

class Eval:
    ''' construct a strategy evaluator '''
    def __init__(self, field='Close', months=12, 
                 init_cash=20000, init_shares=30, min_trade=30, 
                 min_shares=0, min_cash=0, trans_fees=10, 
                 strategy=TrendStrategy(), trade_equal_shares=False,
                 worst=True, min_trade_shares=True,
                 save=False, verbose=False, 
                 debug=False, details=False):
        ''' min trade is either or % in initial_cash or a number of shares '''
        ''' price field = Open, High, Low, Close, Adj Close '''
        
        self.field=field
        self.months=months
        self.init_cash = init_cash
        self.min_cash = min_cash
        if min_cash > init_cash:
            logging.warning("min_cash > init_cash")

        self.init_shares = init_shares
        self.min_shares = min_shares
        if min_shares > init_shares:
            logging.warning("min_share > init_shares")

        self.trade_equal_shares=trade_equal_shares
        self.min_trade = min_trade #if isinstance(min_trade, int) else int(min_trade*init_cash)

        self.trans_fees = trans_fees
        self.set_strategy(strategy)
        self.verbose = verbose
        self.debug = debug
        self.details = details
        self.worst = worst
        self.min_trade_shares = min_trade_shares
        self.save = save
        
    def set_strategy(self, strategy):
        if isinstance(strategy, Strategy):
            self.strategy = strategy
        elif isinstance(strategy, str):
            self.strategy = get_strategy(strategy)
            logging.info("strategy %s" %self.strategy.__class__)

    def set_momentums(cls, buysell='log:log'):
        def get(name):
            if name == 'log':
                return log_momentum
            elif name=='double':
                return double_momentum
            elif name == 'exp':
                return exp_momentum
            else:
                return no_momentum
        buy, sell = buysell.split(":")
        cls.buy_momentum = get(buy)
        cls.sell_momentum = get(sell)
   
    def run(self, stockname, charts=True):
        ''' run the evaluation (strategy = string (old) or Strategy object)'''

        self.stockname = stockname
        if self.verbose:
            print "Evaluation ", self.stockname
    
        # get data
        n = int((5*4)*self.months)
                
        if isinstance(self.strategy, Strategy): 
            
            title = 'automatic strategy base %s' %stockname
            self.orders, self.data = self.strategy.simulate(stockname, n, 
                                                             charts=charts,
                                                             save=self.save)
            if charts:
                plot_orders(self.data[self.field], self.orders, stockname + " (raw orders)")
            if self.save:
                self.strategy.save(stockname, self.orders, self.data.index, 
                                   'orders', verbose=self.verbose)

            self.BackTest(self.orders)
            self.update_starting_point()
            for field in ('trade', 'pnl'):
                self.strategy.save(stockname, self.data[field], self.data.index, 
                                   field, verbose=self.verbose)
            
            if charts:
                plot_orders(self.data[self.field], self.data['trade'], stockname, show=True)
           
            if self.verbose:
                print "------------------------------"
                print "min_cash:",self.min_cash,"min_shares:",self.min_shares
                print "date\norder\ttrade"    
                for d, order,trade in zip(self.data.index, self.orders, self.data['trade']):
                    print d.date(), order, trade

            return self.data.ix[:, header]

                
        else:
            raise Exception("unknown strategy '%s'" %str(self.strategy))
        

    def update_starting_point(self, verbose=False):
        start = self.data.index[0]
        value = self.init_shares*self.data['Adj Close'][0]        
        self.data.set_value(start, 'cash', self.init_cash)
        self.data.set_value(start, 'shares', self.init_shares)
        self.data.set_value(start, 'value', value)
        self.data.set_value(start, 'total', self.init_cash+value)
        self.data.set_value(start, 'pnl', 0)
        if verbose:
            print self.data.ix[:, header]

    def BackTest(self, orders):

        def get_min_trade(i, verbose=False):
            min_trade=self.min_trade
            if not self.min_trade_shares:
                min_trade=round(min_trade/self.data[self.field][i])
                if verbose:
                    logging.info("%s: min trade is set to %s" %(min_trade, self.stockname))
            return min_trade
        
        min_trade=get_min_trade(0, True)

        if self.worst:
            logging.info("set worst trading condition")
            buy_field='High'
            sell_field='Low'
        else:
            buy_field=self.field
            sell_field=self.field

        n = len(orders)
        cash = self.init_cash
        shares = self.init_shares
        cash_available = (cash - self.min_cash) if self.min_cash!=None else MAXINT  
        shares_available = (shares - self.min_shares) if self.min_shares!=None else MAXINT
        
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
                        orders[i] = -self.sell_momentum(orders[i-1])
            return orders[i]

        for i in range(1, len(orders)):
            min_trade=get_min_trade(i)
            order = momentum(orders, i)
            
            if  self.trade_equal_shares:
                trade =  (order*min_trade) - shares
            else:
                trade = (order*min_trade)
                
            trade_value = 0
            if order!=0:
                fees+=self.trans_fees
            # if buy
            if order>0:
                buy_price = self.data[buy_field][i]
                trade_value = trade*buy_price + self.trans_fees
                if (trade_value > cash_available): 
                    trade = int((cash_available-self.trans_fees)/buy_price)
                    trade_value = trade*buy_price + self.trans_fees
            elif order<0: #sell
                if (trade>shares_available):
                    trade = -shares_available
                    
                sell_price = self.data[sell_field][i]
                trade_value = trade*sell_price + self.trans_fees
            # update shares
            shares += trade
            shares_available -= trade
            cash -= trade_value
            cash_available -= trade_value
            self.trades[i] = trade
            self.shares[i] = shares
            self.cash[i] = cash
            self.fees[i] = fees

        # create missing fields
        self.data['shares'] = self.shares
        self.data['cash'] = self.cash
        self.data['trade'] = self.trades
        self.data['fees'] = self.fees
        self.data['value'] = self.data['shares'] * self.data['Open']#TODO['Adj Close']
        self.data['total'] = self.data['cash']+self.data['value']
        self.data['pnl'] = self.data['total']- (self.init_cash+self.init_shares*self.data['Open'])
    
    def __str__(self):
        return str(self.data.ix[:, header])
    
    def eval_best(self, stocks=["TSLA", "GS"], charts=False):
        # try current strategy on different stock
        trademap = {}
        tradedetails = {}
        for i, stock in enumerate(stocks):
            try:
                trade = self.run(stock, charts=charts)
                if False:
                    print i, stock, trade.ix[-1:,'cash':]
                trademap[stock] = trade[-1:]['pnl'][-1]
                tradedetails[stock] = trade[-1:]
            except Exception,ex:
                logging.warning(ex)
        
        st = SortHistogram(trademap, False, True)
        
        if len(stocks)>1:
            print "Here are the Stocks sorted by PnL"
        for i,el in enumerate(st):
            stock, value = el
            print "#", i+1, stock
            print tradedetails[stock].ix[:,header]
        return st

    def plot_field(self, field):
        plot_field(self.data, field, self.stockname)

if __name__ == "__main__":
    print TrendStrategy.apply('TSLA')
    print TrendStrategy.simulate('TSLA', 25)
