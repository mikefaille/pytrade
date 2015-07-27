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

def calc_daily_returns(closes):
    return np.log(closes/closes.shift(1))

def calc_annual_returns(daily_returns):
    grouped = np.exp(daily_returns.groupby(
        lambda date: date.year).sum())-1
    return grouped

class Portfolio:
    ''' simple portfolio class '''
    
    def __init__(self, tickers, weights=None, start=None):
        self.start = date.today() if start==None else start
        weights = np.array(weights) if weights is not None else np.ones(len(tickers))/len(tickers)
        self.tickers = tickers
        self.weights = weights
        self.data = pd.DataFrame({'Tickers': tickers, 
                                  'Weights': weights}, 
                                 index=tickers)
        self._returns = None


    def get_annual_returns(self):
        self.returns
        daily_returns = calc_daily_returns(self.closes)
        return calc_annual_returns(daily_returns)
    
    @property
    def returns(self):
        if self._returns is None:
            from cache import data
            returns = {}
            closes = {}
            for ticker in self.data['Tickers']:
                print "getting ", ticker
                close = data.DataReader(ticker,'yahoo', start=self.start)['Adj Close']
                returns[ticker]=close/close.shift(1)
                closes[ticker]=close
                #returns[ticker] = data.DataReader(ticker,'yahoo', start=self.start)['Adj Close'].diff().fillna(0)
            self._returns = pd.DataFrame(returns)
            self.closes = pd.DataFrame(closes)
        return self._returns

    def plot_returns(self, title=None):
        returns = self.get_weighted_returns() 
        returns.plot(figsize=(12,8))
        plt.xlabel('Year')
        plt.ylabel('Returns')
        if title is not None: plt.title(title)
        plt.show()
    
    def __str__(self):
        print self.data
    
    def get_weighted_returns(self):
        total_weights = self.data.Weights.sum()
        weighted_returns = self.returns * (self.data.Weights / 
                                      total_weights)
        wr = pd.DataFrame({'Value': weighted_returns.sum(axis=1)})
        with_value = pd.concat([self.returns, wr], axis=1)
        return with_value


    def calc_var(self):
        returns = self.returns
        sigma = np.cov(returns.T,ddof=0)
        var = (weights * sigma * self.weights.T).sum()
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
    weights = np.array([46,2.3,25.6,17.5])
    investment_date = '2014-12-01'
    weights /= weights.sum()
    portfolio = Portfolio(tickers, weights, investment_date)
    portfolio.plot_returns()
    print portfolio.get_annual_returns()
    print portfolio.calc_var()
