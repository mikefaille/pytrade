import sys
import time
import urllib2

class Parse(object):
    
    def parse(self, url, stocklist):
        templist = []
        
        delimiter = '&d=t">'
        delimiter2 = '</A>'
        delimiter3 = 'Next'
        
        try:
            req = urllib2.Request(url)
            res = urllib2.urlopen(req)
            output = str(res.read())
            
            # Get list for current results
            splits = output.split(delimiter)
            for item in splits[1:]:
                for thing in item.split(delimiter2):
                    templist.append(thing)
                
        except:
            time.sleep(5)
            self.parse(url, [])
            exit()
            
        count = 0
        for item in templist:
            if count % 3 == 0:
                stocklist.append(item)
            count += 1 
            
        splits = output.split(delimiter3)
        url = url + '&b=1'
        if len(splits) > 1:
            urlsplits = url.split('=')
            urlsplits[-1] = str(int(urlsplits[-1]) + 20)
            url = '='.join(urlsplits)
            self.parse(url, stocklist)
        else:
            return stocklist
