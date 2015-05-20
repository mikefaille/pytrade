''' simulate a buy/sale strategy on a stock & evaluate its PnL (profit and Lost) '''
#!pip install mlboost
import sys
import time
sys.path.append('/usr/local/lib/python2.7/dist-packages')
sys.path.append('/usr/lib/python2.7/dist-packages')
import ConfigParser
from util import evaluate
from stocklist.fetch import Fetch


reload(evaluate)

if len(sys.argv)>1:
    category = sys.argv[1]
else:
    category = 431

#Create database connection
#from db.db import db
#dbconfig = ConfigParser.ConfigParser()
#dbconfig.read('db/db.ini')
#user = dbconfig.get('main', 'user')
#pwd = dbconfig.get('main', 'password')
#dbname = dbconfig.get('main', 'dbname')
#dbconn = db.connect(user, pwd, 'localhost', dbname)

#Fetch stock list from category
fetch = Fetch()
#params is a list of tuples. More info on params can be found in stocklist/filters.py
params = [('sc', category)]
stocks = fetch.fetch_stocks(params)

eval = evaluate.Eval(field='Close', months=1,
                     init_cash=35000, init_shares=40, min_trade=10,
                     min_shares=0, min_cash=0,
                     verbose=True, debug=True);

eval.set_momentums('log','log')
eval.eval_best(stocks, charts=False)

