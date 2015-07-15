from filters import Filter
from parse import Parse
import logging

class Fetch(object):
    
    def fetch_stocks(self, params):
	''' if params==all fetch all stocks get_all_categories'''
        filter = Filter()
        parser = Parse()
        stocklist = []
        if params=='all':
            cats = filter.get_all_categories()
            for cat, desc in cats:
                logging.info('fetching %s (%s)' %(cat, desc))    
                params = [('sc', cat)]
    	        stocklist.extend(self.fetch_stocks(params))
            return stocklist
        else:
            url = filter.build_query_string(params)
            logging.info('url:%s' %url)
	    stocklist = parser.parse(url, stocklist)
	    return stocklist	
	
