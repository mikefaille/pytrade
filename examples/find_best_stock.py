''' find the best stock from choices on which you should apply the strategy 
    base on historic data
'''
#!pip install mlboost
from util import evaluate 
reload(evaluate)

charts = False
verbose = False
months=12

stocks = ["TSLA", "GS", "SCTY", "AMZN", "CSCO",'FB',
          'UTX','JCI',"GOOGL",'BP','MSFT', 'IBM','NUAN','YHOO']
# add oil stock
stocks.extend(["SU", 'TA', 'BP', 'XOM'])

eval = evaluate.Eval(field='Close', months=months, 
                     init_cash=10000, min_trade=40, 
                     verbose=verbose, debug=False);
eval.set_momentums('double','double')
# try current strategy on different stock
out = eval.eval_best(stocks, charts=charts);
  
