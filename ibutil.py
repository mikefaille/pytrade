from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection, message

def error_handler(msg):
    """Handles the capturing of error messages"""
    print("Server Error: %s" % msg)

def reply_handler(msg):
    """Handles of server replies"""
    print("Server Response: %s, %s" % (msg.typeName, msg))


def create_contract(symbol, sec_type, exch, prim_exch, curr):
    """Create a Contract object defining what will
    be purchased, at which exchange and in which currency.

    symbol - The ticker symbol for the contract
    sec_type - The security type for the contract ('STK' is 'stock')
    exch - The exchange to carry out the contract on
    prim_exch - The primary exchange to carry out the contract on
    curr - The currency in which to purchase the contract"""
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = curr
    return contract

def create_order(order_type, quantity, action):
    """Create an Order object (Market/Limit) to go long/short.

    order_type - 'MKT', 'LMT' for Market or Limit orders
    quantity - Integral number of assets to order
    action - 'BUY' or 'SELL'"""
    order = Order()
    order.m_orderType = order_type
    order.m_totalQuantity = quantity
    order.m_action = action
    return order

import pickle
import os
class IB:
    def __init__(self, clientId=999):
        self.tws_conn = Connection.create(port=7496, clientId=clientId)
        self.tws_conn.connect()
        self.tws_conn.register(error_handler, 'Error')
        self.tws_conn.registerAll(reply_handler)
        self.ib_orderid_fname="ib_orderid_fname.p"
        if os.path.isfile(self.ib_orderid_fname):
            self.order_id = pickle.load(open(self.ib_orderid_fname, 'rb'))
        else:
            self.order_id = 1

    def save_order_id(self):
        pickle.dump(self.order_id, open(self.ib_orderid_fname, 'wb'))

    def create_order(self, stock="TSLA", order=99):
        action = 'BUY' if order>0 else 'SELL'
        # Create a contract in GOOG stock via SMART order routing
        goog_contract = create_contract(stock, 'STK', 'SMART', 'SMART', 'USD')

        # Go long 100 shares of Google
        goog_order = create_order('MKT', abs(order), action)
        
        # Use the connection to the send the order to IB
        self.tws_conn.placeOrder(self.order_id, goog_contract, goog_order)
        print("order %s %s" %(self.order_id, stock)) 
	self.order_id+=1
	self.save_order_id()

    def close(self):
        # Disconnect from TWS
        tws_conn.disconnect()

if __name__ == "__main__":
    ib = IB()
    ib.create_order()
    
