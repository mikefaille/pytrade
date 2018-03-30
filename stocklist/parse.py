import sys
import time
import urllib2

class Parse(object):

    def parse(self, url, stocklist, first_pass = True):
        templist = []
        
        delimiter = '&d=t">'
        delimiter2 = '</A>'
        delimiter3 = 'Next'
        
        try:
            req = urllib2.Request(url)
            res = urllib2.urlopen(req)
            output = str(res.read())
       
	except urllib2.HTTPError, error: 
            contents = error.read()
	    print(contents)
	    
        except:
	    print(sys.exc_info()[0])
            time.sleep(5)
            self.parse(url, [])
            exit()
            
        # Get list for current results
	splits = output.split(delimiter)
	for item in splits[1:]:
	    for thing in item.split(delimiter2):
		templist.append(thing)

        count = 0
	
        for item in templist:
            if count % 3 == 0:
                stocklist.append(item)
            count += 1 
            
        splits = output.split(delimiter3)
        if first_pass:
            url = url + '&b=1'
        if len(splits) > 1:
            print(url)
            urlsplits = url.split('=')
            urlsplits[-1] = str(int(urlsplits[-1]) + 20)
            url = '='.join(urlsplits)
            self.parse(url, stocklist, False)
	    return stocklist
        else:
            return stocklist
