 #!/usr/bin/python
''' generate dataset '''
import csv
import argparse
import numpy as np
import sklearn.metrics
import theanets
from sklearn.metrics import accuracy_score
import logging
from trendStrategy import OptTrendStrategy
def load_dataset(stock, ratio=0.8, name=OptTrendStrategy.__name__):
    ''' return train, valid (x,y) '''
    orders = np.loadtxt("{0}_{1}_orders.csv".format(stock, name), usecols=[1], delimiter=',')
    orders[orders==-1]=0
    features = np.loadtxt("{0}_input.csv".format(stock), delimiter=',')
    if len(orders)!=len(features):
        logging.error("len(orders)!=len(features) -> %s!=%s" %(len(orders),len(features)))
    features = features.astype('f')
    orders = orders.astype('i')
    pos = round(len(features)*ratio)
    train = (features[:pos], orders[:pos])
    valid = (features[pos:], orders[pos:])
    return train, valid

def evaluate(exp, dataset):
    y_true = dataset[1]
    y_pred = exp.network.predict(dataset[0])
    print(sklearn.metrics.confusion_matrix(y_true, y_pred))
    print('accuracy:',accuracy_score(y_true, y_pred))
    
def train_strategy(stock, ratio=0.8, min_improvement=0.001):
    
    train, valid = load_dataset(stock)
    n, n_input = train[0].shape

    exp = theanets.Experiment(
        theanets.Classifier,
        layers=(n_input, n_input*2, 2),
    )
    exp.train(train, valid, min_improvement=min_improvement,
            algo='sgd',
            learning_rate=0.01,
            momentum=0.5,
            hidden_l1=0.001,
            weight_l2=0.001,
            num_updates=100
    ) 
    print('training:')
    evaluate(exp, train)
    
    print('validation:')
    evaluate(exp, valid)
    
    exp.save('%s.nn' %stock)
    return exp
    
def load_strategy(name, verbose=False):
    print("loading %s trained strategy" %name)
    train, valid = load_dataset(name) 
    n, n_input = train[0].shape
    exp = theanets.Experiment(
        theanets.Classifier,
        layers=(n_input, n_input*2, 2),
    )
    exp.load('%s.nn' %name)
    if verbose:
        print('training:')
        evaluate(exp, train)
        print('validation:')
        evaluate(exp, valid)
    return exp
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stock', '-s', default="TSLA", help='stock')
    parser.add_argument('--ratio', '-r', default=0.8, type=int, help='train/valid ratio')
    parser.add_argument('--min', '-m', default=0.001, type=int, help='min improvement (stop learning)')
    args = parser.parse_args()
    
    train, valid = load_dataset(args.stock)
    exp = train_strategy(args.stock, args.ratio, args.min)
    exp = load_strategy(args.stock, True)
