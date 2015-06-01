 #!/usr/bin/python
''' generate dataset '''
import csv
import argparse
import numpy as np

def load_dataset(stock, ratio=0.8):
    ''' return train, valid (x,y) '''
    orders = np.loadtxt("{0}_orders.csv".format(stock), usecols=[1], delimiter=',')
    orders[orders==-1]=0
    features = np.loadtxt("{0}_input.csv".format(stock), delimiter=',')
    features = features.astype('f')
    orders = orders.astype('i')
    pos = round(len(features)*ratio)
    train = (features[:pos], orders[:pos])
    valid = (features[pos:], orders[pos:])
    return train, valid

def train_strategy(stock, ratio=0.8):
    import sklearn.metrics
    import theanets
    
    train, valid = load_dataset(args.stock)
    n, n_input = train[0].shape

    exp = theanets.Experiment(
        theanets.Classifier,
        layers=(n_input, n_input*2, 2),
    )
    #exp.train(train, valid, min_improvement=0.001)
    exp.train(train, valid, min_improvement=0.01,
            algo='sgd',
            learning_rate=0.01,
            momentum=0.5,
            hidden_l1=0.001,
            weight_l2=0.001,
            num_updates=100
    ) 
    print('training:')
    print(sklearn.metrics.confusion_matrix(
        train[1], exp.network.predict(train[0])))
    
    print('validation:')
    print(sklearn.metrics.confusion_matrix(
        valid[1], exp.network.predict(valid[0])))
    return exp
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stock', '-s', default="TSLA", help='stock')
    parser.add_argument('--ratio', '-r', default=0.8, type=int, help='train/valid ratio')
    args = parser.parse_args()
    
    train, valid = load_dataset(args.stock)
    exp = train_strategy(args.stock, args.ratio)
