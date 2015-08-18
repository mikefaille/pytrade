 #!/usr/bin/python
''' evaluate portfolio risk module 
leveraging http://dx-analytics.com/
'''
import pandas as pd
import argparse
import logging

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--stocks', '-s', default="TSLA", help='list of stocks (comma separated)')
parser.add_argument('--verbose', '-v', action="store_true", help='verbose')
parser.add_argument('--details', action="store_true", help='add details')
parser.add_argument('--debug', '-d', action="store_true", help='debug')
parser.add_argument('--logging_info', action="store_true", help='activate logging.info')

args = parser.parse_args()

if args.logging_info:
    logging.basicConfig(level=logging.INFO)

if ":" in args.stocks:
    weights = dict([el.split(':') for el in args.stocks.split(',')])
else:
    weights = dict([(el,1) for el in args.stocks.split(',')])

#normalize weights
total = sum([float(el) for el in weights.values()])
for ticker in weights:
    weights[ticker]=float(weights[ticker])/total

print weights
    
    
  
