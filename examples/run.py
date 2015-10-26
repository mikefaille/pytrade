 #!/usr/bin/python
''' run does 3 things:
 #1) eval a strategy on a stock -> ./run.py -s TSLA (default) 
 #2) find best stock:   ./run.py --stock TSLA,GS,SCTY,AMZN,TWTR 
                        ./run.py --cat 431 --fetch_limit 5 
 #3) buy or sale today: ./run.py --stock TSLA,GS,SCTY,AMZN,TWTR --now 
 #4) download data    : ./run.py --download
find the best stock from choices on which you should apply the strategy 
    base on historic data 
# 5) generate best, train, try 
python run.py -s TSLA --best --save --charts --details --months 36 
python run.py -s TSLA --save --pnl
python run.py -s TSLA --train
python run.py -S GS --load TSLA --details 

other: 
python  examples/run.py --month 12 -s TSLA --charts --details --fees 0 --momentum none:none --shares --min_trade 10 --best  --ts --init_shares 10
'''
import sys
from util import evaluate 
reload(evaluate)
import pandas as pd
import argparse
import logging
from util.strategy import Strategy 
from util.dataset import load_strategy, train_strategy

pd.set_option('precision', 3) 
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--stocks', '-s', default="TSLA", help='list of stocks (comma separated)')
parser.add_argument('--months', '-m', default=12, type=int, help='history nb of months')
parser.add_argument('--init_cash', default=10000, type=int, help='initial cash')
parser.add_argument('--init_shares', default=40, type=int, help='min trade')
parser.add_argument('--min_trade', default=1000, type=int, help='min trade (default=$)')
parser.add_argument('--min_shares', default=0, type=int, help='min shares')
parser.add_argument('--min_cash', default=0, type=int, help='min cash')
parser.add_argument('--fees', default=10, type=int, help='min fees')
parser.add_argument('--verbose', '-v', action="store_true", help='verbose')
parser.add_argument('--details', action="store_true", help='add details')
parser.add_argument('--debug', '-d', action="store_true", help='debug')
parser.add_argument('--charts', '-c', action="store_true", help='show charts')
parser.add_argument('--cat', default=None, type=int, help='fetch stocks from categy (ex:431)')
parser.add_argument('--fetch_limit', default=None, type=int, help='fetch limit nb of stocks')
parser.add_argument('--momentums', default="log:log", 
                    help='momentums x:x (x=log, exp, double, none)')
parser.add_argument('--load', default=None, help='load trained strategy')
parser.add_argument('--train', action="store_true", help='train strategy')
parser.add_argument('--test', action="store_true", help='test example stocks')
parser.add_argument('--strategy', default='trend', help='strategy to apply')
parser.add_argument('--now', action="store_true", help='get buy/sale now')
parser.add_argument('--logging_info', action="store_true", help='activate logging.info')
parser.add_argument('--ts', action="store_true", help='trades = shares')
parser.add_argument('--best', action="store_true", help='best algo')
parser.add_argument('--worst', action="store_true", help='worst selling scenarios')
parser.add_argument('--save', action="store_true", help='save strategy')
parser.add_argument('--ref', action="store_true", help='ref ideal case')
parser.add_argument('--shares', action="store_true", help='min trade is in shares')
parser.add_argument('--pnl', action="store_true", help='show PnL (profit and lost"')
parser.add_argument('--field', default='Open', help='price field = Open, High, Low, Close, Adj Close')
parser.add_argument('--ib', action="store_true", help='send order on ib')
parser.add_argument('--download', action="store_true", help='download all stock categories')

def main(args=None):
    args = args.split(' ') or sys.argv[1:]
    args = parser.parse_args(args)

    if args.best:
        args.strategy='opt_trend'

    if args.logging_info:
        logging.basicConfig(level=logging.INFO)

    if args.ref:
        print "activating ref ideal case"
        args.stocks="TSLA"
        args.months=12
        args.charts=True
        args.details=True
        args.init_shares=0
        args.ts=True
        args.fees=0
        args.momentum="none:none"
        args.shares=True
        args.min_trade=10
        args.best=True
        
    if args.best:
        args.strategy="opt_trend"

    eval = evaluate.Eval(field=args.field, months=args.months, 
                         init_cash=args.init_cash, init_shares=args.init_shares,
                         min_trade=args.min_trade,trans_fees=args.fees,
                         min_cash=args.min_cash, min_shares=args.min_shares, 
                         strategy=args.strategy, details=args.details,
                         worst=args.worst, min_trade_shares=args.shares,
                         trade_equal_shares=args.ts,
                         save=args.save,
                         verbose=args.verbose, debug=args.debug)

    eval.set_momentums(args.momentums)
      
    if args.load:
        exp = load_strategy(args.load)
        eval.strategy.predict = exp.network.predict
    
    from stocklist.fetch import Fetch
    fetch = Fetch()
    
    if args.download:
        stocks = fetch.fetch_stocks('all')
    elif args.cat!=None:
        print "category", args.cat
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
            order = eval.strategy.apply(stock)
            print stock,"->", order
            if args.ib:
                from ibutil import IB
                ib=IB()
                ib.create_order(stock)

    # evaluate strategy on different stocks 
    elif len(stocks)>1:
        eval.min_trade_shares=False
        eval.eval_best(stocks, charts=args.charts)
    else: # evalue strategy 
        if args.train:
            eval.save=True;eval.set_strategy('opt_trend')
            print "generating optimal orders"
            eval.run(stocks[0], charts=False)
            print "generating features"
            eval.save=True;eval.set_strategy('opt_trend')
            eval.run(stocks[0], charts=False)
            print "training"
            train_strategy(stocks[0])
        else:
            eval.run(stocks[0], charts=args.charts)
        if args.pnl or args.details:
            eval.plot_field('pnl')
        print eval

if __name__ == "__main__":
    main()
    
  
