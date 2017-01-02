# http://docs.python.org/3.2/library/pprint.html

import pprint 
import cryptsy.api
import cryptsy.market
import cryptsy.bot

## Key file to access an account
key_file = "cryptsy1.txt"
account = cryptsy.api.Account(key_file)
api = cryptsy.api.Api(account)
mk = cryptsy.market.Market(api, 'BTC', 'NMC')

orders = mk.my_orders()
balances = mk.balances()


pprint.pprint(orders)
pprint.pprint(balances)
