 #!/usr/bin/python
''' alarm does alarm you on stock major price variation
'''
import pandas as pd
import argparse
import logging

from util.cache import data
from stocklist.fetch import Fetch
pd.set_option('precision', 3) 
default_tickers = 'TSLA,SCTY,AMZN,TWITR,NFLX,BABA,BIDU,GRN,PE,AAPL,GOOGL' 

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--stocks', '-s', default=default_tickers, 
                    help='list of stocks (comma separated)')
parser.add_argument('--download', action="store_true", 
                    help='download all stock categories')
parser.add_argument('--cat', default=None, type=int, 
                    help='fetch stocks from categy (ex:431)')
parser.add_argument('--window', default=15, type=int, 
                    help='window nb of day used')
parser.add_argument('--test', action="store_true", help='test example stocks')
parser.add_argument('--logging_info', action="store_true", help='activate logging.info')
args = parser.parse_args()

if args.logging_info:
    logging.basicConfig(level=logging.INFO)

fetch = Fetch()

if args.download:
    stocks = fetch.fetch_stocks('all')
elif args.cat!=None:
    print("category", args.cat)
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


for stock in stocks:
    print(stock)
    previous = data.DataReader(stock, 'google', lastn=args.window)
    std = previous.pct_change()[1:].std()
    


    #previous = history(context.window, "1d", field='price')
    #std = previous.pct_change()[1:].std()
    #yesterday_close = history(2, '1d', 'price').iloc[0]
