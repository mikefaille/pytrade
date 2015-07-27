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
            for cat in cats:
                params = [('sc', cat)]
                try:
                    stocklist.extend(self.fetch_stocks(params))
                except Exception, e:
                    print cat 
                    print e
                    #print stocklist
                    print 'exited prematurely'
                    exit()
        else:
            url = filter.build_query_string(params)
            logging.info('url:%s' %url)
            print url
	    stocklist = parser.parse(url, stocklist)

        return stocklist	
	
if __name__ == "__main__":
    fetch = Fetch()
    #params = [('sc', 812)]
    params = 'all'
    result = fetch.fetch_stocks(params)
