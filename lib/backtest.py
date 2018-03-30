#-------------------------------------------------------------------------------
# Name:        backtest
# Purpose:     perform routine backtesting  tasks. 
#              This module should be useable as a stand-alone library outide of the TWP package.
#
# Author:      Jev Kuznetsov
#
# Created:     03/07/2014
# Copyright:   (c) Jev Kuznetsov 2013
# Licence:     BSD
#-------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np

def tradeBracket(price, entryBar, upper=None, lower=None, timeout=None):
    '''
    trade a  bracket on price series, return price delta and exit bar #
    Input
    ------
        price : numpy array of price values
        entryBar: entry bar number, *determines entry price*
        upper : high stop
        lower : low stop
        timeout : max number of periods to hold

    Returns exit price  and number of bars held

    '''
    assert isinstance(price, np.ndarray) , 'price must be a numpy array'
    
    
    # create list of exit indices and add max trade duration. Exits are relative to entry bar
    if timeout: # set trade length to timeout or series length
        exits = [min(timeout,len(price)-entryBar-1)]
    else:
        exits = [len(price)-entryBar-1] 
        
    p = price[entryBar:entryBar+exits[0]+1] # subseries of price
    
    # extend exits list with conditional exits
    # check upper bracket
    if upper:
        assert upper>p[0] , 'Upper bracket must be higher than entry price '
        idx = np.where(p>upper)[0] # find where price is higher than the upper bracket
        if idx.any(): 
            exits.append(idx[0]) # append first occurence
    # same for lower bracket
    if lower:
        assert lower<p[0] , 'Lower bracket must be lower than entry price '
        idx = np.where(p<lower)[0]
        if idx.any(): 
            exits.append(idx[0]) 
   
    exitBar = min(exits) # choose first exit    

    return p[exitBar], exitBar


class Backtest(object):
    """ Backtest class, simple vectorized one. Works with pandas objects.
    """    
    def __init__(self, price, signal, signalType='capital', 
                 initialCash = 0, initialShares=0, 
                 min_shares=0, min_cash=0, trans_fees=10,
                 roundShares=True):
        """
        Arguments:
        
        *price*  Series with instrument price.
        *signal* Series with capital to invest (long+,short-) or number of shares. 
        *sitnalType* capital to bet or number of shares 'capital' mode is default.
        *initialCash* starting cash. 
        *roundShares* round off number of shares to integers
        
        """
        def constraints(min_shares, min_cash, verbose=False):
            shares = initialShares
            cash = initialCash
            for i, trade in enumerate(self.trades):
                # check you can really sell shares
                if min_shares!=None and trade<0 and (shares+trade)<=min_shares:
                    self.trades[i]=-(shares+min_shares)
                # check you can really buy shares
                elif min_cash!=None and trade>0 and (trade*price[i]+trans_fees>cash):
                    self.trades[i]=round((cash-trans_fees)/price[i])
                
                shares+=self.trades[i]
                cash-=self.trades[i]*price[i]+trans_fees
                if verbose:
                    print(i, trade, "->", self.trades[i], shares)

        #TODO: add auto rebalancing
        
        # check for correct input
        signal_choices = ['capital','shares', "orders"]
        assert signalType in signal_choices, "Wrong signal type provided, must be %s" %' or '.join(signal_choices)
        
        #save internal settings to a dict
        self.settings = {'signalType':signalType}
        
        # first thing to do is to clean up the signal, removing nans and duplicate entries or exits
        self.signal = signal.ffill().fillna(0)
        
        # now find dates with a trade
        if signalType in ('shares', 'capital'):
            self.trades = self.signal.diff().fillna(0)
            tradeIdx = self.trades != 0 # days with trades are set to True
            if signalType == 'capital':
                self.trades = (self.signal[tradeIdx]/price[tradeIdx]).reindex(self.data.index).ffill().fillna(0)
            if roundShares:
                self.trades = self.trades.round()
        elif signalType == 'orders':
            self.trades = self.signal
        
        # now create internal data structure 
        self.data = pd.DataFrame(index=price.index , columns = ['trades','price','shares','value','cash','total','pnl'])
        self.data['price'] = price
        
        if min_shares!=None or min_cash!=None:
            constraints(min_shares, min_cash)
        else:
            # add trade fees
            tradeIdx = self.trades != 0 
            self.signal[tradeIdx]+=trans_fees

        self.data['trades'] = self.trades
        self.data['shares'] = self.trades.cumsum()+initialShares
        self.data['value'] = self.data['shares'] * self.data['price']

        delta = self.data['shares'].diff() # shares bought sold
        
        self.data['cash'] = (-delta*self.data['price']).fillna(0).cumsum()+initialCash
        self.data['pnl'] = self.data['cash']+self.data['value']-initialCash
        self.data['total'] = self.data['cash']+self.data['value']
      
    @property
    def sharpe(self):
        ''' return annualized sharpe ratio of the pnl '''
        pnl = (self.data['pnl'].diff()).shift(-1)[self.data['shares']!=0] # use only days with position.
        return sharpe(pnl)  # need the diff here as sharpe works on daily returns.
        
    @property
    def pnl(self):
        '''easy access to pnl data column '''
        return self.data['pnl']
    
    def plotTrades(self, name='', style='orders'):
        """ 
        visualise trades on the price chart 
            long entry : green triangle up
            short entry : red triangle down
            exit : black circle
        """
        l = ['price']
        
        p = self.data['price']
        p.plot(style='x-')
        
        # ---plot markers
        # this works, but I rather prefer colored markers for each day 
        # of position rather than entry-exit signals        
        if style=='orders':
            indices = {'g^': self.trades[self.trades > 0].index , 
                       'ko':self.trades[self.trades == 0].index, 
                       'rv':self.trades[self.trades < 0].index}
            

            for style, idx in indices.iteritems():
                if len(idx) > 0:
                    p[idx].plot(style=style)
        else:
        
            # --- plot trades
            #colored line for long positions
            idx = (self.data['shares'] > 0) | (self.data['shares'] > 0).shift(1) 
            if idx.any():
                p[idx].plot(style='go')
                l.append('long')
        
            #colored line for short positions    
            idx = (self.data['shares'] < 0) | (self.data['shares'] < 0).shift(1) 
            if idx.any():
                p[idx].plot(style='ro')
                l.append('short')

            plt.xlim([p.index[0],p.index[-1]]) # show full axis
            plt.legend(l, loc='best')

        plt.title('trades for %s' %name)
        
class ProgressBar:
    def __init__(self, iterations):
        self.iterations = iterations
        self.prog_bar = '[]'
        self.fill_char = '*'
        self.width = 50
        self.__update_amount(0)

    def animate(self, iteration):
        print('\r',self)
        sys.stdout.flush()
        self.update_iteration(iteration + 1)

    def update_iteration(self, elapsed_iter):
        self.__update_amount((elapsed_iter / float(self.iterations)) * 100.0)
        self.prog_bar += '  %d of %s complete' % (elapsed_iter, self.iterations)

    def __update_amount(self, new_amount):
        percent_done = int(round((new_amount / 100.0) * 100.0))
        all_full = self.width - 2
        num_hashes = int(round((percent_done / 100.0) * all_full))
        self.prog_bar = '[' + self.fill_char * num_hashes + ' ' * (all_full - num_hashes) + ']'
        pct_place = (len(self.prog_bar) // 2) - len(str(percent_done))
        pct_string = '%d%%' % percent_done
        self.prog_bar = self.prog_bar[0:pct_place] + \
            (pct_string + self.prog_bar[pct_place + len(pct_string):])
    
    def __str__(self):
        return str(self.prog_bar)
    
def sharpe(pnl):
    return  np.sqrt(250)*pnl.mean()/pnl.std()

