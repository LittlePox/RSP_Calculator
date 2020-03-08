from datetime import datetime
from datetime import date


class ProductQuote:
    def __init__(self, product_id, cob_date, close, nav):
        self.product_id = product_id
        if isinstance(cob_date, date):
            self.cob_date = cob_date
        else:
            self.cob_date = datetime.strptime(cob_date, "%Y-%m-%d")
        self.close = close
        self.nav = nav

    def __str__(self):
        return 'ProductQuote[' + ','.join(str(x) for x in [self.product_id, self.cob_date, self.close, self.nav])

    def db_save_command(self):
        return "insert or replace into PRODUCT_QUOTE values ({0}, '{1}', {2}, {3})".format(
            self.product_id, self.cob_date.strftime(
                "%Y-%m-%d"), self.close, self.nav
        )
