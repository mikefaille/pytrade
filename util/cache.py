import os
import logging
import pickle
import pandas.io.data as pdata

class DataCache(object):

    datadir = os.path.dirname(os.path.realpath(__file__)) + '/../data'

    def __init__(self):
        self.cache = {}
	   

    def DataReader(self, name, data_source="yahoo", start=None, end=None):
        datafilepath = self.datadir + '/' + name + '.p'
        def get_date_range(start,end):
            start = start if start is not None else self.cache[name].index[0]
            end = end if end is not None else self.cache[name].index[-1]
            return self.cache[name][start:end]

        if name in self.cache:
	    logging.info('Retreiving ' + name + ' from cache')
            return get_date_range(start, end)
        elif os.path.isfile(datafilepath):
            self.cache[name] = pickle.load(open(datafilepath, "rb"))
	    logging.info('Retreiving ' + name + ' from file')
            return get_date_range(start, end)
        else:
            data = pdata.DataReader(name, data_source)
            self.cache[name] = data
            pickle.dump(data, open(datafilepath,"wb"))
	    logging.info('Retreiving ' + name + ' from internet and stored')
            return get_date_range(start, end)


if __name__ == "__main__":
    dc = DataCache()
    print dc.DataReader('TSLA')

