 #!/usr/bin/python
''' evaluate portfolio risk module 
leveraging http://dx-analytics.com/
http://dx-analytics.com/11_dx_mean_variance_portfolio.html
'''
import numpy as np
import pandas as pd
import argparse
import logging
from datetime import date, timedelta
import matplotlib.pyplot as plt
from dx import *

def visualize(port, n_stock, n=500):
    # Monte Carlo simulation of portfolio compositions
    rets = []
    vols = []
    
    for w in range(n):
        weights = np.random.random(n_stock)
        weights /= sum(weights)
        r, v, sr = port.test_weights(weights)
        rets.append(r)
        vols.append(v)

    rets = np.array(rets)
    vols = np.array(vols)
    
    plt.scatter(vols, rets, c=rets / vols, marker='o')
    evols, erets = port.get_efficient_frontier(100)
    plt.scatter(evols, erets, c=erets / evols, marker='x')
    plt.grid(True)
    plt.xlabel('expected volatility')
    plt.ylabel('expected return')
    plt.colorbar(label='Sharpe ratio')
    plt.show()


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--stocks', '-s', default="TSLA:2,TWTR:1,AMZN:1,BABA:1,BIDU:1", help='list of stocks (comma separated)')
parser.add_argument('--verbose', '-v', action="store_true", help='verbose')
parser.add_argument('--details', action="store_true", help='add details')
parser.add_argument('--end', default=date.today(), help='end date')
parser.add_argument('--start', default=date.today()-timedelta(days=365), help='start date')
parser.add_argument('--debug', '-d', action="store_true", help='debug')
parser.add_argument('--logging_info', action="store_true", help='activate logging.info')

args = parser.parse_args()

if args.logging_info:
    logging.basicConfig(level=logging.INFO)

if ":" in args.stocks:
    weights = dict([el.split(':') for el in args.stocks.split(',')])
else:
    weights = dict([(el,1) for el in args.stocks.split(',')])

#normalize weights
total = sum([float(el) for el in weights.values()])
for ticker in weights:
    weights[ticker]=float(weights[ticker])/total
print weights
    
# create marker_environment    
ma = market_environment('ma', args.start)
ma.add_list('symbols', weights.keys())
ma.add_constant('source', 'google')
ma.add_constant('final date', args.end)
port = mean_variance_portfolio('am_tech_stocks', ma)
visualize(port, len(weights))
port.set_weights(weights.values())



def eval_port(name):
    print "evaluation %s" %name 
    print port
    print "return = ",port.get_portfolio_return()

eval_port("default distribution")
for opt in ["Return", 'Vol', 'Sharpe']:
    port.optimize(opt)
    eval_port("Optimize %s" %opt)
    #port.optimize('Return', constraint=0.225, constraint_type='Exact')
    #port.optimize('Return', constraint=0.4, constraint_type='Bound')
