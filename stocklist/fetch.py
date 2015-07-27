from filters import Filter
from parse import Parse
import logging

class Fetch(object):
    
    def fetch_stocks(self, params):
	''' if params==all fetch all stocks get_all_categories'''
        filter = Filter()
        parser = Parse()
        if params=='all':
            cats = filter.get_all_categories()
            stocklist = []
            for cat in cats:
                logging.info('fetching %s' % cat)    
                params = [('sc', cat)]
    	        stocks = self.fetch_stocks(params)
                for stock in stocks:
		    stocklist.append(stock)
	    print stocklist
	    exit()
            return cats
        else:
            url = filter.build_query_string(params)
	    stocklist = []
	    stocklist = parser.parse(url, stocklist)
	    return stocklist	
	
