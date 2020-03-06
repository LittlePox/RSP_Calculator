from datetime import datetime

class ProductQuote:
    def __init__(self, product_id, cob_date, close, nav):
        self.product_id = product_id
        self.cob_date = datetime.strptime(cob_date, "%Y-%m-%d").date()
        self.close = close
        self.nav = nav

    def __str__(self):
        return 'ProductQuote[' + ','.join(str(x) for x in [self.product_id, self.cob_date, self.close, self.nav])