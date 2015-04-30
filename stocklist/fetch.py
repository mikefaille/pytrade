from filters import Filter
from parse import Parse

class Fetch(object):
    
    def fetch_stocks(self, params):
        filter = Filter()
        parser = Parse()
        
        url = filter.build_query_string(params)
        results = parser.parse(url, [])
