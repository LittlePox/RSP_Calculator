from datetime import datetime, date, timedelta


class ProductInvestment:
    def __init__(self, product_id, week_start, base_amount, level):
        self.product_id = product_id
        if isinstance(week_start, date):
            self.week_start = week_start
        else:
            self.week_start = datetime.strptime(week_start, '%Y-%m-%d').date()
        self.base_amount = base_amount
        self.level = level
        self.actual_amount = base_amount
        if level > 0:
            self.actual_amount = int(base_amount * 1.5 ** level)
        else:
            self.actual_amount = int(base_amount * 0.5 ** (-level))

    def __str__(self):
        return 'ProductInvestment[{0},{1},{2},{3},{4}]'.format(
            self.product_id, self.week_start.strftime(
                '%Y-%m-%d'), self.base_amount, self.level, self.actual_amount
        )

    def db_save_command(self):
        return "INSERT OR REPLACE INTO PRODUCT_INVESTMENT VALUES ({0},'{1}',{2},{3})".format(
            self.product_id, self.week_start.strftime(
                '%Y-%m-%d'), self.base_amount, self.level
        )
