import numpy as np
import math
from scipy.special import ndtri
from random import random
# based on https://www.youtube.com/watch?v=e79OtCamxD0
# ln(S/S-1)= drift + rand * vol
# drift = expected return for the stock
def walk(n=1000, annual_drift=.1, annual_volatility=.4, init_price=100, 
         verbose=False):
    drift = float(annual_drift)/252
    vol = float(annual_volatility)/np.sqrt(252)
    drift_mean = drift-0.5*math.pow(vol,2)
    prices = np.zeros(n)
    if verbose:
        print "drift:", drift
        print "volatility:", vol
        print "drift mean:", drift_mean
    previous_price = init_price
    for i in range(n):
        r = random()
        z = ndtri(r)
        log_return = drift+vol*z
        price = previous_price*math.exp(log_return)
        if verbose:
            print "#%i r=%.2f z=%.2f ret=%.2f%% price=%.2f$" %(i, r, z, log_return*100, price)
        previous_price = price
        prices[i]=price

    return prices
    
    
if __name__=="__main__":
    n = 1000
    confidence = 99.0
    prices = np.array([walk()[-1] for i in range(n)])
    prices.sort()
    Si = prices[round((100-confidence)/100*n) ]
    VaR = Si - prices[0] 
    print "Si=%.2f Lowest=%.2f VaR=%.2f" %(Si, prices[0], VaR)
    
