from strategy import Strategy
from trendy import segtrends
from strategy import *

class twpStrategy(Strategy):
     
    @classmethod
    def visu(cls, stockname, save=False):
        from pylab import title, figure, savefig, subplot, show
        print("#1) Automatic buy/sales visualisation of the current strategy (buy=long, short=sale)")
        if save:
            subplot(211)
        else:
            figure()
        cls.backtest.plotTrades(stockname)
        print("#2) Evaluation of the strategy (PnL (Profit & Log) = Value today - Value yesterday)")
        if save:
            subplot(212)
        else:
            figure()
        cls.backtest.pnl.plot()
        title('pnl '+stockname)
        if save:
            savefig('eval.png')
        
        print("#3) big picture: Price, shares, value, cash & PnL")
        cls.backtest.data.plot()
        title('all strategy data %s' %stockname)
        if save:
            savefig('all.png')
        else:
            show()

    @classmethod
    def orders2strategy(cls, orders, price, min_stocks=1):
        strategy = pd.Series(index=price.index) 
        orders=[el*min_stocks for el in orders]
        # create a stratgy from order
        for i, idx in enumerate(price.index):
            if orders[i]!=0:
                strategy[idx] = orders[i]
        return strategy

    @classmethod
    def orders_from_trends(cls, x, segments=2, charts=True, window=7, 
                           sell_momentum=no_momentum, 
                           buy_momentum=no_momentum,
                           title=None):
        ''' generate orders from segtrends '''
        x_maxima, maxima, x_minima, minima = segtrends(x, segments, charts, window, title)
        n = len(x)
        y = np.array(x)
        movy = movingaverage(y, window)
        
        # generate order strategy
        orders = np.zeros(n)
        last_buy = y[0]
        last_sale = y[0]
        
        for i in range(1,n):
            # get 2 latest support point y values prior to x
            pmin = list(minima[np.where(x_minima<=i)][-2:])
            pmax = list(maxima[np.where(x_maxima<=i)][-2:])
            # sell if support slop is negative
            min_sell = True if ((len(pmin)==2) and (pmin[1]-pmin[0])<0) else False 
            max_sell = True if ((len(pmax)==2) and (pmax[1]-pmax[0])<0) else False 

            # if support down, sell
            buy = -1 if (min_sell and max_sell) else 0
            # buy only if lower the moving average else sale
            buy = 1 if ((buy == 0) and (y[i]<movy[i])) else -1
            # sell only if ... # MUCH BETTER WITHOUT IT
            #buy= -1 if ((buy == -1) and y[i]>last_buy) else 1
      
            buy_price_dec = y[i]<last_buy
            sale_price_dec = y[i]<last_sale
            orders[i] = buy
            last_buy = y[i] if (buy==1) else last_buy
            last_sale = y[i] if (buy==-1) else last_sale
        
            
            # add momentum for buy 
            if buy_momentum and (buy==1) and (orders[i-1]>=1):
                #if buy_price_dec:
                #orders[i]=orders[i-1]*2#round(math.log(2*orders[i-1])+1)
                orders[i]=buy_momentum(orders[i-1])#round(math.log(2*orders[i-1])+1)
                #else:
                #   orders[i]=max(1, round(orders[i-1]/2))
                # add momentum for sale
            elif sell_momentum and (buy==-1) and (orders[i-1]<=-1):
                #if sale_price_dec:
                #orders[i]*=round(math.log(abs(orders[i-1]*2))+1)
                orders[i]=-sell_momentum(orders[i-1])
                #else:
                #    orders[i]=max(1, round(orders[i-1]/2))
        
        # ensure no order are taken at the begining
        for i in range(window):
            orders[i]=0
        return orders
