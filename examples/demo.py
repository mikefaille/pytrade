''' simulate a buy/sale strategy on a stock & evaluate its PnL (profit and Lost) '''
#!pip install mlboost
import sys
from util import strategy
reload(strategy)

if len(sys.argv)>1:
    stock = sys.argv[1]
else:
    #stock ="AAPL"
    #stock='TA' #oil
    #stock='BP' # oil
    stock = 'TSLA'

eval = strategy.Eval(field='Close', months=12, 
                     init_cash=35000, init_shares=100, min_trade=10,
                     min_shares=None, min_cash=None,
                     verbose=True, debug=True);
#eval.set_momentums('double','double')
eval.set_momentums('log','log')
#eval.set_momentums('exp','exp')
summary = eval.run(stock, charts=True, signalType='orders', save=False)
#summary.to_csv('%s.csv' %stock)
print stock, summary.ix[-1:,'cash':]
