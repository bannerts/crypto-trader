## http://docs.python.org/3.3/library/urllib.html
from urllib.request import urlopen

## http://docs.python.org/3.3/library/json.html
import json

## http://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python
import time, datetime

## btc-e.com urls

URLS = {
    'btc-e.com': {}, 
    'mtgox.com': {}, 
    'coinbase.com': {}
}

for item in ['ticker', 'trades', 'depth']:
    url_dict = {item:
        {
        'btc_usd': 'https://btc-e.com/api/2/btc_usd/{}'.format(item),
        'ltc_btc': 'https://btc-e.com/api/2/ltc_btc/{}'.format(item),
        'nmc_btc': 'https://btc-e.com/api/2/nmc_btc/{}'.format(item),
        'nvc_btc': 'https://btc-e.com/api/2/nvc_btc/{}'.format(item),
        'trc_btc': 'https://btc-e.com/api/2/trc_btc/{}'.format(item),
        'ppc_btc': 'https://btc-e.com/api/2/ppc_btc/{}'.format(item),
        'ftc_btc': 'https://btc-e.com/api/2/ftc_btc/{}'.format(item),
        'xpm_btc': 'https://btc-e.com/api/2/xpm_btc/{}'.format(item),
        }
    }
    URLS['btc-e.com'].update(url_dict)

def get_data( exchange, name ): 
    result = {}
    for item in ['ticker', 'trades', 'depth']:
        with urlopen(URLS[exchange][item][name]) as url:
            http_info = url.info()
            raw_data = url.read().decode(http_info.get_content_charset())
        url_info = json.loads(raw_data)
        if item != 'trades':
            result.update(url_info)
        else:
            result.update({'trades': url_info})
    
    meta = {'traded': [name[0:3], name[-3:]], 'name': name} 
    result.update(meta) 
    
    bids = result['bids']
    asks = result['asks']
    
    if len(bids) > 0:
        bid_depth = [bids[0]]
        for i in range(1, len(bids)):
            bid = bids[i]
            bid_depth.append([bid[0], bid_depth[-1][1]])
            bid_depth.append([bid[0], bid[1]+bid_depth[-1][1]])
    if len(asks) > 0:
        ask_depth = [asks[0]]
        for i in range(1, len(asks)):
            ask = asks[i]
            ask_depth.append([ask[0], ask_depth[-1][1]])
            ask_depth.append([ask[0], ask[1]+ask_depth[-1][1]])
    
    bid_depth.reverse()
    data = bid_depth + ask_depth
    price = []
    depth = []
    for i in range(len(data)):
        price.append(data[i][0])
        depth.append(data[i][1])    
    market_depth = {'market depth': [price, depth]}
    result.update(market_depth)
        
    return result
    
    
    
    
