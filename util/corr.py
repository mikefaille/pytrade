import numpy as np
from util import cache
import pandas as pd

def correlation(stocks, field='Adj Close'):
    data = pd.DataFrame({stocks[0]:cache.data.DataReader(stocks[0])[field]})
    for stock in stocks[1:]:
        data = data.join(pd.DataFrame({stock:cache.data.DataReader(stock)[field]}))
    data=data.fillna(method='ffill')
    rets = np.log(data/data.shift(1))
    return rets.corr()

if __name__ == "__main__":
    stocks = ["TSLA", "GS", "SCTY", "AMZN", "CSCO",'FB',
              'UTX','JCI',"GOOGL",'BP','MSFT', 'IBM','NUAN','YHOO']
    print correlation(stocks)
                          
                
        
