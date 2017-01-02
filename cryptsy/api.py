## cryptsy.com api

## http://docs.python.org/3.3/library/urllib.html
import urllib.request
import urllib.parse

## http://docs.python.org/3.3/library/json.html
import json
## http://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python
import time, datetime
import hmac, hashlib

api_urls = {'public':  'http://pubapi.cryptsy.com/api.php',
        'private': 'https://api.cryptsy.com/api',
        }

class Account:
    def __init__(self, key_file):
        self.key_file = key_file
        keys = get_keys(self.key_file)
        self.key = keys["key"]
        self.secret = keys["secret"]
        self.url = api_urls['private']

    # issue any supported query (method: string, req: dictionary with method parameters)
    def Query(self, method, req = {}):

        # Generate post data
        req["method"] = method
        req["nonce"] = int(time.time())
        post_data = urllib.parse.urlencode(req)
        post_data = post_data.encode('utf-8')
        
        # sign it
        sign = hmac.new(self.secret.encode(), post_data, hashlib.sha512).hexdigest()
        # Add Headers for request
        headers = { "Sign": sign, 
                    "Key": self.key, 
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                    }

        X = urllib.request.Request(self.url, post_data, headers)        
        response = urllib.request.urlopen(X)
        response_data = response.read()
        response_json = json.loads(response_data.decode('utf-8'))           
        if response_json['success'] == '1':
            return (True, response_json['return'])
        else:
            return (False, response_json['error'])


def get_keys(key_file):
    keys = {}
    with open(key_file, 'rt') as f:
        keys["key"] = f.readline().strip()
        keys["secret"] = f.readline().strip()
    return keys

class Api:
    def __init__(self, account):
        self.Query = account.Query
        self.MARKETS = {}  # {currency: {coin: marketid}}
        self.COINS = {}      # {symbol: name}
        self.CURRENCIES = {} # {symbol: name}
        self.MARKETIDS = {}  # {id: {"label":, "currency":, "coin": }
        self.get_data()
   
    def get_data(self):
        success, marketdata = self.getmarkets()

        if not success:
            return
        for m in marketdata:
            coin = m['primary_currency_code']
            coin_name = m['primary_currency_name']
            currency = m['secondary_currency_code']
            currency_name = m['secondary_currency_name']
            marketid = m['marketid']
            label = m['label']
            # Market Dictionary
            self.MARKETIDS[marketid] = {'label': label, 'currency': currency, 'coin': coin}
            # Create coins & currencies dictionary
            self.COINS[coin] = coin_name
            self.CURRENCIES[currency] = currency_name
            # Create exchanges dictionary
            if currency in self.MARKETS:
                self.MARKETS[currency][coin] = marketid
            else:   
                self.MARKETS[currency] = {coin: marketid}    

    def get_balances(self, coins = False):
        if not coins:
            coins = self.COINS
        success, info = self.getinfo()
        balances = {}
        if not success:
            return balances
        available = info['balances_available']
        on_hold = info['balances_hold']
        for coin in coins:
            balances[coin] = {'available': available.get(coin, 0),
                              'hold': on_hold.get(coin, 0) }
        return balances

    def getinfo(self):
        return self.Query( "getinfo")

    def getmarkets(self):
        return self.Query( "getmarkets")

    def getwalletstatus(self):
        return self.Query( "getwalletstatus")

    def mytransactions(self):
        return self.Query( "mytransactions")

    def markettrades(self, marketid):
        x = {"marketid": marketid}
        return self.Query( "markettrades", x)

    def marketorders(self, marketid):
        x = {"marketid": marketid}        
        return self.Query( "marketorders", x)

    def mytrades(self, marketid, limit = 200):
        x = {"marketid": marketid, "limit": limit}     
        return self.Query( "mytrades", x)

    def allmytrades(self, startdate = "yyyy-mm-dd",  enddate = "yyyy-mm-dd"):
        x = {}
        if startdate != "yyyy-mm-dd":
            x["startdate"] = startdate
        if enddate != "yyyy-mm-dd":
            x["enddate"] = enddate 
        return self.Query( "allmytrades", x)

    def myorders(self, marketid):
        x = {"marketid": marketid}        
        return self.Query( "myorders", x)

    def depth(self, marketid = ""):
        x = {"marketid": marketid}        
        return self.Query( "depth", x)

    def allmyorders(self):
        return self.Query( "allmyorders")

    ## ORDER CREATION METHODS
    def createorder(self, marketid, ordertype, quantity, price):
        x = {"marketid": marketid,
            "ordertype": ordertype,
            "quantity": quantity,
            "price": price,
            }
        return self.Query( "createorder", x)
    
    def buy(self, quantity, price, marketid):
        return self.createorder(marketid, "Buy", quantity, price)
        
    def sell(self, quantity, price, marketid):
        return self.createorder(marketid, "Sell", quantity, price)

    def calculatefees(self, ordertype, quantity, price):
        x = {"ordertype": ordertype,
            "quantity": quantity,
            "price": price,
            }
        return self.Query("calculatefees", x)
        
    def cancelorder(self, orderid):
        x = {"orderid": orderid}
        return self.Query( "cancelorder", x)

    def cancelmarketorders(self, marketid):
        x = {"marketid": marketid}
        return self.Query( "cancelmarketorders", x)

    def cancelallorders(self):
        return self.Query( "cancelallorders") 
