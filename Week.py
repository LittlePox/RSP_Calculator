from datetime import datetime, date, timedelta


class Week:
    def __init__(self, any_day):
        self.start = any_day - timedelta(days=any_day.weekday())
        self.end = self.start + timedelta(days=6)

    def prev_week(self):
        return Week(self.start - timedelta(days=1))

    def next_week(self):
        return Week(self.end + timedelta(days=1))

    def __str__(self):
        return 'Week[{0}, {1}]'.format(self.start.strftime('%Y-%m-%d'), self.end.strftime('%Y-%m-%d'))
