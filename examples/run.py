 #!/usr/bin/python
''' run does 3 things:
 #1) eval a strategy on a stock -> ./run.py -s TSLA (default) \
 #2) find best stock:  ./run.py --stock TSLA,GS,SCTY,AMZN,TWTR \
                       ./run.py --cat 431 --fetch_limit 5 \
 #3) by or sale today: ./run.py --stock TSLA,GS,SCTY,AMZN,TWTR --now \
\
find the best stock from choices on which you should apply the strategy \
    base on historic data \
'''
from util import evaluate 
reload(evaluate)
import pandas as pd
import argparse
import logging

pd.set_option('precision', 3) 
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--stocks', '-s', default="TSLA", help='list of stocks (comma separated)')
parser.add_argument('--months', '-m', default=12, type=int, help='history nb of months')
parser.add_argument('--init_cash', default=10000, type=int, help='initial cash')
parser.add_argument('--init_shares', default=40, type=int, help='min trade')
parser.add_argument('--min_trades', default=10, type=int, help='min trade')
parser.add_argument('--min_shares', default=None, type=int, help='min shares')
parser.add_argument('--min_cash', default=None, type=int, help='min cash')
parser.add_argument('--verbose', '-v', action="store_true", help='verbose')
parser.add_argument('--details', action="store_true", help='add details')
parser.add_argument('--debug', '-d', action="store_true", help='debug')
parser.add_argument('--charts', '-c', action="store_true", help='show charts')
parser.add_argument('--cat', default=None, type=int, help='fetch stocks from categy (ex:431)')
parser.add_argument('--fetch_limit', default=None, type=int, help='fetch limit nb of stocks')
parser.add_argument('--momentums', default="log:log", help='momentums x:x (x=log, exp, double, none)')
parser.add_argument('--test', action="store_true", help='test example stocks')
parser.add_argument('--strategy', default='trend', help='strategy to apply')
parser.add_argument('--now', action="store_true", help='get buy/sale now')
parser.add_argument('--logging_info', action="store_true", help='activate logging.info')
parser.add_argument('--ts', action="store_true", help='trades = shares')

args = parser.parse_args()
eval = evaluate.Eval(field='Close', months=args.months, 
                     init_cash=args.init_cash, min_trades=args.min_trades,
                     min_cash=args.min_cash, min_shares=args.min_shares, 
                     strategy=args.strategy, details=args.details,
                     trade_equal_shares=args.ts,
                     verbose=args.verbose, debug=args.debug);
eval.set_momentums(args.momentums)
if args.logging_info:
    logging.basicConfig(level=logging.INFO)


      
if args.cat!=None:
    print "category", args.cat
    from stocklist.fetch import Fetch
    fetch = Fetch()
    #params is a list of tuples. More info on params can be found in stocklist/filters.py
    params = [('sc', args.cat)]
    stocks = fetch.fetch_stocks(params)
    if args.fetch_limit!=None:
        stocks=stocks[:args.fetch_limit]
elif args.test:
    stocks = ["TSLA", "GS", "SCTY", "AMZN", "CSCO",'FB',
              'UTX','JCI',"GOOGL",'BP','MSFT', 'IBM','NUAN','YHOO']
    # add oil stock
    stocks.extend(["SU", 'TA', 'BP', 'XOM'])
else:
    stocks = args.stocks.split(',')

# should you trade it now?
if args.now:
    for stock in stocks:
        print stock,"->",eval.strategy.apply(stock)
# evaluate strategy on different stocks 
elif len(stocks)>1:
    eval.eval_best(stocks, charts=args.charts)
else: # evalue strategy 
    eval.run(stocks[0], charts=args.charts)
    if args.charts and args.details:
        eval.plot_field('pnl')
    print eval
    
    
  
