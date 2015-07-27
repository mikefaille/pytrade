# various pandas, numpy
import pandas as pd
import numpy as np
import pandas.io.data as web
from datetime import datetime, date
import scipy as sp
import scipy.optimize as scopt
import scipy.stats as spstats
import matplotlib.mlab as mlab
# plotting
import matplotlib.pyplot as plt


class Portfolio:
    ''' simple portfolio class '''
    
    def __init__(self, tickers, weights=None, start=None):
        self.start = date.today() if start==None else start
        if weights is None: 
            shares = np.ones(len(tickers))/len(tickers)
        self.data = pd.DataFrame({'Tickers': tickers, 
                                  'Weights': weights}, 
                                  index=tickers)

    def get_returns(self):
        from cache import data
        returns = {}
        for ticker in self.data['Tickers']:
            print "getting ", ticker
            returns[ticker] = data.DataReader(ticker,'yahoo', start=self.start)['Adj Close'].diff().fillna(0)
        return returns

    def __str__(self):
        print self.data
    
    def calculate_weighted_portfolio_value(self, start_date=None, name='Value'):
        total_weights = self.data.Weights.sum()
        returns = self.get_returns()
        weighted_returns = returns * (self.data.Weights / 
                                      total_weights)
        return pd.DataFrame({name: weighted_returns.sum(axis=1)})

def plot_portfolio_returns(returns, title=None):
    returns.plot(figsize=(12,8))
    plt.xlabel('Year')
    plt.ylabel('Returns')
    if title is not None: plt.title(title)
    plt.show()

def calc_daily_returns(closes):
    return np.log(closes/closes.shift(1))

def calc_annual_returns(daily_returns):
    grouped = np.exp(daily_returns.groupby(
        lambda date: date.year).sum())-1
    return grouped

def calc_portfolio_var(returns, weights=None):
    if weights is None: 
        weights = np.ones(returns.columns.size) / \
        returns.columns.size
    sigma = np.cov(returns.T,ddof=0)
    var = (weights * sigma * weights.T).sum()
    return var

def sharpe_ratio(returns, weights = None, risk_free_rate = 0.015):
    n = returns.columns.size
    if weights is None: weights = np.ones(n)/n
    # get the portfolio variance
    var = calc_portfolio_var(returns, weights)
    # and the means of the stocks in the portfolio
    means = returns.mean()
    # and return the sharpe ratio
    return (means.dot(weights) - risk_free_rate)/np.sqrt(var)

def negative_sharpe_ratio_n_minus_1_stock(weights, 
                                          returns, 
                                          risk_free_rate):
    """
    Given n-1 weights, return a negative sharpe ratio
    """
    weights2 = sp.append(weights, 1-np.sum(weights))
    return -sharpe_ratio(returns, weights2, risk_free_rate)

def optimize_portfolio(returns, risk_free_rate):
    """ 
    Performs the optimization
    """
    # start with equal weights
    w0 = np.ones(returns.columns.size-1, 
                 dtype=float) * 1.0 / returns.columns.size
    # minimize the negative sharpe value
    w1 = scopt.fmin(negative_sharpe_ratio_n_minus_1_stock, 
                    w0, args=(returns, risk_free_rate))
    # build final set of weights
    final_w = sp.append(w1, 1 - np.sum(w1))
    # and calculate the final, optimized, sharpe ratio
    final_sharpe = sharpe_ratio(returns, final_w, risk_free_rate)
    return (final_w, final_sharpe)

def objfun(W, R, target_ret):
    stock_mean = np.mean(R,axis=0)
    port_mean = np.dot(W,stock_mean) # portfolio mean
    cov=np.cov(R.T) # var-cov matrix
    port_var = np.dot(np.dot(W,cov),W.T) # portfolio variance
    penalty = 2000*abs(port_mean-target_ret)# penalty 4 deviation
    return np.sqrt(port_var) + penalty # objective function

def calc_efficient_frontier(returns):
    result_means = []
    result_stds = []
    result_weights = []
    
    means = returns.mean()
    min_mean, max_mean = means.min(), means.max()
    
    nstocks = returns.columns.size
    
    for r in np.linspace(min_mean, max_mean, 100):
        weights = np.ones(nstocks)/nstocks
        bounds = [(0,1) for i in np.arange(nstocks)]
        constraints = ({'type': 'eq', 
                        'fun': lambda W: np.sum(W) - 1})
        results = scopt.minimize(objfun, weights, (returns, r), 
                                 method='SLSQP', 
                                 constraints = constraints,
                                 bounds = bounds)
        if not results.success: # handle error
            raise Exception(result.message)
        result_means.append(np.round(r,4)) # 4 decimal places
        std_=np.round(np.std(np.sum(returns*results.x,axis=1)),6)
        result_stds.append(std_)
        
        result_weights.append(np.round(results.x, 5))
    return {'Means': result_means, 
            'Stds': result_stds, 
            'Weights': result_weights}


if __name__ == "__main__":
    from cache import data
    tickers = ['BABA','DBA','TSLA','TWTR']
    weights = np.array([44,2.1,26,17])  
    weights /= weights.sum()
    #closes = data.get_historical_closes(tickers)
    #daily_returns = calc_daily_returns(closes)
    #annual_returns = calc_annual_returns(daily_returns)

    portfolio = Portfolio(tickers, weights)
    portfolio.calculate_weighted_portfolio_value(portfolio)
