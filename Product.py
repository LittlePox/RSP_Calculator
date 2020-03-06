class Product:
    def __init__(self, id, name, currency, wsjTicker, yahooTicker):
        self.id = id
        self.name = name
        self.currency = currency
        self.wsjTicker = wsjTicker
        self.yahooTicker = yahooTicker
    
    def __str__(self):
        return 'Product[' + ','.join(str(x) for x in (self.id, self.name, self.currency, self.wsjTicker, self.yahooTicker)) + "]"
