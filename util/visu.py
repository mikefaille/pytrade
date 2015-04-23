import numpy as np
import matplotlib.pyplot as plt

def plot_orders(data, orders, stockname, show=True):
    data.plot(style='x-')
    indices = {'g^': np.where(orders > 0)[0], 
               'ko': np.where(orders == 0)[0], 
               'rv': np.where(orders < 0)[0]}
    
    
    for style, idx in indices.iteritems():
        if len(idx) > 0:
            data[idx].plot(style=style)
            
    import matplotlib.pyplot as plt
    plt.title("Orders for %s" %stockname)
    if show:
        plt.show()
