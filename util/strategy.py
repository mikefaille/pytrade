import numpy as np
import pandas as pd
import math

import pandas.io.data as pdata
from datetime import timedelta
from datetime import date
from visu import plot_orders

# little hack to make in working inside heroku submodule
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

log_momentum = lambda previous: round(math.log(1+2*abs(previous))+1)
double_momentum = lambda previous: 2*abs(previous)
exp_momentum = lambda previous: round(math.pow(abs(previous), 2))
no_momentum = lambda previous:round(abs(previous))

import abc

class Strategy:
    __metaclass__ = abc.ABCMeta
    field = 'Close'
    window = 7
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
