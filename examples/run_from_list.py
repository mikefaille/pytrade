''' simulate a buy/sale strategy on a stock & evaluate its PnL (profit and Lost) '''
#!pip install mlboost
import sys
import time
sys.path.append('/usr/local/lib/python2.7/dist-packages')
sys.path.append('/usr/lib/python2.7/dist-packages')
import ConfigParser
from util import strategy
from stocklist.fetch import Fetch
from db.db import db

reload(strategy)

if len(sys.argv)>1:
    category = sys.argv[1]
else:
    category = 431

#Create database connection
dbconfig = ConfigParser.ConfigParser()
dbconfig.read('db/db.ini')
user = dbconfig.get('main', 'user')
pwd = dbconfig.get('main', 'password')
dbname = dbconfig.get('main', 'dbname')
dbconn = db.connect(user, pwd, 'localhost', dbname)

#Fetch stock list from category
fetch = Fetch()
#params is a list of tuples. More info on params can be found in stocklist/filters.py
params = [('sc', category)]
result = fetch.fetch_stocks(params)

eval = strategy.Eval(field='Close', months=1,
                     init_cash=35000, init_shares=40, min_trade=10,
                     min_shares=0, min_cash=0,
                     verbose=True, debug=True);

eval.set_momentums('log','log')

for stock in result:
    #Run strategy on stock
    try:
        summary = eval.run(stock, charts=False, signalType='orders', save=False)
        print stock
        print "Start\n",summary.ix[0]#:,'cash':]
        print "end",summary.ix[-1]
        print summary
        time.sleep(3)
 
    except IOError:
	continue

