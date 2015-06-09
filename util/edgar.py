import json
import urllib2

class Edgar():

    def __init__(self):
        self.app_key = []
	self.app_key.append('gt92w3z25c8ep9375p2mrsqa')
        
    
    def get_financial_docs(self, stock, type='ann', limit=None):
	url = 'http://edgaronline.api.mashery.com/v2/corefinancials/ann?'
        url += 'primarysymbols=' + stock
        url += '&appkey=' + self.app_key[0]
        
        json_data = urllib2.urlopen(url).read()
        return json.loads(json_data)
        

if __name__ == "__main__":
    edgar = Edgar()
    data = edgar.get_financial_docs('AAPL')
    
    for key in data['result']['rows'][0]['values']:
            print key['field']
            print key['value']
