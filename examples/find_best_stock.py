''' find the best stock from choices on which you should apply the strategy 
    base on historic data
'''
#!pip install mlboost
from util import evaluate 
reload(evaluate)

stocks = ["TSLA", "GS", "SCTY", "AMZN", "CSCO",'FB',
          'UTX','JCI',"GOOGL",'BP','MSFT', 'IBM','NUAN','YHOO']
# add oil stock
stocks.extend(["SU", 'TA', 'BP', 'XOM'])


import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--stocks', '-s', default=None, help='list of stocks (comma separated)')
parser.add_argument('--months', '-m', default=12, help='history nb of months')
parser.add_argument('--init_cash', default=10000, type=int, help='initial cash')
parser.add_argument('--min_trade', default=40, type=int, help='min trade')
parser.add_argument('--verbose', '-v', action="store_true", help='verbose')
parser.add_argument('--debug', '-d', action="store_true", help='debug')
parser.add_argument('--charts', '-c', action="store_true", help='show charts')
parser.add_argument('--cat', default=None, type=int, help='fetch stocks from categy')

args = parser.parse_args()
eval = evaluate.Eval(field='Close', months=args.months, 
                     init_cash=args.init_cash, min_trade=args.min_trade, 
                     verbose=args.verbose, debug=args.debug);
eval.set_momentums('double','double')

if args.cat!=None:
    print "category", args.cat
    from stocklist.fetch import Fetch
    fetch = Fetch()
    #params is a list of tuples. More info on params can be found in stocklist/filters.py
    params = [('sc', args.cat)]
    stocks = fetch.fetch_stocks(params)
else:
    stocks = stocks


# try current strategy on different stock
out = eval.eval_best(stocks, charts=args.charts);
  
