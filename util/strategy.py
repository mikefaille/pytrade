import numpy as np
import pandas as pd
import math
import csv
import logging

import pandas.io.data as pdata
from datetime import timedelta, date
from visu import plot_orders
from util.cache import DataCache

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
    datacache = DataCache()
    predict = None

    @abc.abstractmethod
    def apply(self, stock, data=None, writer=None):
        """ return buy(1) or sell(-1) """
        return

    @classmethod
    def get_data(self, stock, start, end=None, npoints=False, verbose=False):
        end = end if end!=None else date.today()-timedelta(days=1)
        if isinstance(start, int):
            if npoints:
                data = self.datacache.DataReader(stock, "yahoo")[-start:]
            else:
                start = end-timedelta(days=start)
                 # add required padding 
                data = self.datacache.DataReader(stock, "yahoo",
                                                start=start-timedelta(days=self.window),
                                                end=end)
        if verbose:
            print "period:", start, end, ";ndays =",(end-start).days
       
        return data

    def simulate(self, stock, start=None, end=None, npoints=False, 
                 charts=True, verbose=False, save=True):
        ''' start is a datetime or nb days prior to now '''
        logging.info(sys._getframe().f_code.co_name)
        writer =  csv.writer(open('%s_input.csv' %stock, 'wb')) if save else None
        data = self.get_data(stock, start, end, npoints, verbose=verbose)
        start = data.index[0]+timedelta(days=self.window)
        end = data.index[-1]
                                
        n = len(data)-self.window+1
        orders=np.zeros(n)
       
        # ensure orders[0]=0 (initial point)
        for i in range(1,  n):
            start_i = start+timedelta(days=-self.window+i)
            end_i = start+timedelta(days=i)
            data_i = data[start_i:end_i]
            order = self.apply(stock, data_i, writer)
            orders[i]=order
            if verbose:
                print end_i+timedelta(days=1), order
        
        if charts:
            p = data[self.field][-n:]
            plot_orders(p, orders, stock + " (raw orders)")
        
        return orders, data[-n:]    
       
            
