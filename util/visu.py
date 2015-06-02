import numpy as np
import matplotlib.pyplot as plt

def compare(a, b, title=None):
    x = range(len(a))
    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
    ax1.plot(x, a)
    ax2.plot(x, b)
    ax3.plot(x, a-b)
    if title:
        ax1.set_title(title)
    plt.show()

def plot_orders(data, orders, stockname, show=True):
    plt.figure()
    data.plot(style='x-')
    indices = {'g^': np.where(orders > 0)[0], 
               'ko': np.where(orders == 0)[0], 
               'rv': np.where(orders < 0)[0]}
    
    
    for style, idx in indices.iteritems():
        if len(idx) > 0:
            data[idx].plot(style=style)
    
    plt.title("Orders for %s" %stockname)
    if show:
        plt.show()


def plot_field(data, field, name="", show=True):
    plt.title(field+" "+name)
    data[field].plot()
    if show:
        plt.show()
