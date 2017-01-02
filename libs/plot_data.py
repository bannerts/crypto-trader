## http://matplotlib.org/1.3.1/users/pyplot_tutorial.html

import matplotlib.pyplot as plt
import pprint


def market_depth(name, save = False):
    price = name['market depth'][0]
    depth = name['market depth'][1]


    plt.xlabel('Price ({0})'.format(name['traded'][1]))  
    plt.ylabel('Depth ({0})'.format(name['traded'][0]))
    plt.title('Market Depth ({0})'.format(name['name']))
    plt.plot(price, depth)
    N = int(len(depth)/10)
    plt.axis([price[0], price[-1], 0, max(depth[N:])])

    plt.show()
    if save:
        plt.savefig(name['name'] + '.png')
        plt.close()
    return 

def trading(data, save=False):
    trades = data['trades']
    bids = []
    asks = []
    for trade in trades:
        price = trade['price']
        amount = trade['amount']
        type = trade['trade_type']
        time = trade['date']
        if type == 'bid':
            bids.append([time, price, amount])
        elif type == 'ask':
            asks.append([time, price, amount])
    
    t_bid, price_bid, amount_bid = [], [], []
    for bid in bids[-1::-1]:
        t_bid.append(bid[0])
        price_bid.append(bid[1])
        amount_bid.append(bid[2])
    
    t_ask, price_ask, amount_ask = [], [], []
    for ask in asks[-1::-1]:
        t_ask.append(ask[0])
        price_ask.append(ask[1])
        amount_ask.append(ask[2])
    
    plt.xlabel('time')  
    plt.ylabel('Amount')
    plt.plot(t_bid, price_bid, 'g^', t_ask, price_ask, 'ro')
    
    plt.show()       
    
    return 
    
