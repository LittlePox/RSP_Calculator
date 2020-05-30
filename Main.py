from Product import Product
import sqlite3
import pathlib
from WsjCrawler import WsjCrawler
from Crawler import Crawler
from datetime import date, timedelta, datetime
from Week import Week
from ProductQuote import ProductQuote, get_daily_returns, get_weekly_return
from ProductInvestment import ProductInvestment

cur_dir = str(pathlib.Path(__file__).parent.absolute())
conn = sqlite3.connect(cur_dir + '/database.db')
cur = conn.cursor()

products = []
cur.execute("select * from PRODUCT")
for i in cur.fetchall():
    products.append(Product(i[0], i[1], i[2], i[3], i[4]))

crawler = WsjCrawler()

for p in products:
    for x in crawler.crawl(p):
        cur.execute(x.db_save_command())
conn.commit()

print("Crawling done.")

today = (datetime.today() + timedelta(days=1, hours=16)).date()
this_week = Week(today)
weeks = []
for i in range(0, 100):
    this_week = this_week.prev_week()
    weeks.append(this_week)
weeks.reverse()
this_week = Week(today)

for p in products:
    print("Analyzing {0}".format(p.name))

    cur.execute(
        "select * from PRODUCT_QUOTE where PRODUCT_ID = {0} order by COB_DATE DESC LIMIT 1000".format(
            p.id)
    )
    quotes = []
    for i in cur.fetchall():
        quotes.append(ProductQuote(i[0], i[1], i[2], i[3]))
    quotes.reverse()

    week_rets = [get_weekly_return(quotes, w) for w in weeks]
    last_week_ret = week_rets[len(weeks) - 1]
    this_week_ret = get_weekly_return(quotes, this_week)
    print("last week return: {:.2f}%".format(week_rets[len(weeks) - 1] * 100))
    print("this week return: {:.2f}%".format(this_week_ret * 100))
    lamb = 0.98
    week_weights = [1]
    for i in range(1, len(weeks) - 1):
        week_weights.append(week_weights[i - 1] * lamb)
    week_weights.reverse()
    nomalizer = sum(week_weights)
    week_weights = [x / nomalizer for x in week_weights]
    weighted_ret = []
    for i in range(0, len(weeks) - 1):
        weighted_ret.append((week_rets[i], week_weights[i]))
    weighted_ret.sort()

    quantile = [0.03, 0.15, 0.30, 0.70, 0.85, 0.97, 1.01]
    idx = 0
    pos = 4
    total = 0
    for i in range(0, len(weeks) - 1):
        total += weighted_ret[i][1]
        if total >= quantile[idx]:
            print("{:.2f}% quantile: {:.2f}%".format(
                quantile[idx] * 100, (weighted_ret[i][0] + weighted_ret[max(i - 1, 0)][0]) * 50)
            )
            idx = idx + 1
        if weighted_ret[i][0] >= last_week_ret and pos == 4:
            pos -= idx + 1
    if pos == 4:
        pos = -3
    print("Level adjustment: {0}".format(pos))

    ivst = None
    cur.execute(
        "select * from PRODUCT_INVESTMENT where PRODUCT_ID = {0} order by WEEK_START DESC LIMIT 1".format(
            p.id)
    )
    for i in cur.fetchall():
        ivst = ProductInvestment(i[0], i[1], i[2], i[3])
    if ivst is None:
        print("No investment has been made.")
    elif ivst.week_start == this_week.start:
        print("Investment has been made this week with level = {0} and amount = {1}".format(
            ivst.level, ivst.actual_amount))
    else:
        new_level = ivst.level
        if new_level > 0:
            new_level = new_level - 1
        elif new_level < 0:
            new_level = new_level + 1
        new_level += pos
        new_level = min(3, max(-3, new_level))

        print("original level: {0}, new level: {1}".format(
            ivst.level, new_level))

        new_ivst = ProductInvestment(
            p.id, this_week.start, ivst.base_amount, new_level)
        print("Investment should be made this week with amount = {}".format(
            new_ivst.actual_amount))
        cur.execute(new_ivst.db_save_command())
        conn.commit()

    print("Finised {0}".format(p.name))
    print()

print("Finished all products.")
conn.close()
