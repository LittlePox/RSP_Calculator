from datetime import datetime
from datetime import date
from Week import Week


class ProductQuote:
    def __init__(self, product_id, cob_date, close, nav):
        self.product_id = product_id
        if isinstance(cob_date, date):
            self.cob_date = cob_date
        else:
            self.cob_date = datetime.strptime(cob_date, "%Y-%m-%d").date()
        self.close = close
        self.nav = nav

    def __str__(self):
        return 'ProductQuote[' + ','.join(str(x) for x in [self.product_id, self.cob_date.strftime('%Y-%m-%d'), self.close, self.nav]) + ']'

    def db_save_command(self):
        return "insert or replace into PRODUCT_QUOTE values ({0}, '{1}', {2}, {3})".format(
            self.product_id, self.cob_date.strftime(
                "%Y-%m-%d"), self.close, self.nav
        )


def get_daily_returns(quotes):
    rets = []
    for i in range(1, len(quotes)):
        rets.append(quotes[i].nav / quotes[i - 1].nav - 1)
    return rets


def get_weekly_return(quotes, week):
    l = 0
    r = len(quotes) - 1
    idx = 0
    while l <= r:
        m = (l + r) // 2
        if quotes[m].cob_date < week.start:
            idx = m
            l = m + 1
        else:
            r = m - 1
    r = idx + 1
    while r + 1 < len(quotes) and quotes[r + 1].cob_date <= week.end:
        r = r + 1
    return quotes[r].nav / quotes[idx].nav - 1
