class Market:
    def __init__(self, api, currency = "BTC", coin = "DOGE"):
        self.api = api
        self.marketid = api.MARKETS[currency][coin]
        self.currency = currency
        self.coin = coin

    def set_currency(self, x):
        self.currency = x
        self.marketid = api.MARKETS[self.currency][self.coin]

    def set_coin(self, x):
        self.coin = coin
        self.marketid = api.MARKETS[self.currency][self.coin]

    def market_orders(self):
        success, orders = self.api.marketorders(self.marketid)

        if not success:
            return
        sells = [(s['sellprice'], s['quantity']) for s in orders['sellorders']]
        buys = [(b['buyprice'], b['quantity']) for b in orders['buyorders']]
        return {'Buy': buys, 'Sell': sells}

    def balances(self):
        return self.api.get_balances((self.currency, self.coin))

    def my_orders(self):
        success, orders = self.api.myorders(self.marketid)
        if not success:
            return
        buys = []
        sells = []
        for order in orders:
            price = order['price']
            quantity = order['quantity']
            orderid = order['orderid']
            if order['ordertype'] == 'Buy':
                buys.append((price, quantity, orderid))
            if order['ordertype'] == 'Sell':
                sells.append((price, quantity, orderid))
        buys = sorted(buys, key=lambda x: -x[0])
        sells = sorted(sells, key=lambda x: x[0])
        return {'Buy': buys, 'Sell': sells}


    def cancel(self, orderid = ""):
        if orderid == "":
            self.api.cancelmarketorders(self.marketid)
        else:
            self.api.cancelorder(orderid)
 
    def fees(self, quantity, price):
        success1, buyfee = self.api.calculatefees('Buy', quantity, price)
        success2, sellfee = self.api.calculatefees('sell', quantity, price)
        if not (success1 and success2):
            return
        return (buyfee['fee'], buyfee['net'], sellfee['fee'], sellfee['net'])


