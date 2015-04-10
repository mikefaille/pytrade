''' simulate a buy/sale strategy on a stock & evaluate its PnL (profit and Lost) '''
#!pip install mlboost
import sys
from util import strategy 
reload(strategy)

charts = True
verbose = True
debug = True
signalType = 'shares'
months = 12

if len(sys.argv)>1:
    stock = sys.argv[1]
else:
    #stock ="AAPL"
    #stock='TA' #oil
    #stock='BP' # oil
    stock = 'TSLA'

eval = strategy.Eval(field='open', months=months, 
                     initialCash=20000, min_stocks=40, 
                     verbose=verbose, debug=True);
eval.set_momentums('double','double')
summary = eval.run(stock, charts=charts, signalType=signalType)

print stock, summary.ix[-1:,'cash':]
