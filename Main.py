from Product import Product
import sqlite3
import pathlib
from WsjCrawler import WsjCrawler
from Crawler import Crawler
from datetime import date, timedelta, datetime
from Week import Week
from ProductQuote import ProductQuote, get_daily_returns, get_weekly_return

cur_dir = str(pathlib.Path(__file__).parent.absolute())
conn = sqlite3.connect(cur_dir + '/database.db')
cur = conn.cursor()

products = []
cur.execute("select * from PRODUCT")
for i in cur.fetchall():
    products.append(Product(i[0], i[1], i[2], i[3], i[4]))

crawler = Crawler()

for p in products:
    for x in crawler.crawl(p):
        cur.execute(x.db_save_command())
conn.commit()

print("Crawling done.")

today = datetime.today().date()
thisweek = Week(today)
weeks = []
for i in range(0, 100):
    thisweek = thisweek.prev_week()
    weeks.append(thisweek)
weeks.reverse()

for p in products:
    print("Analyzing {0}".format(p.name))
    cur.execute(
        "select * from PRODUCT_QUOTE where PRODUCT_ID = {0} order by COB_DATE DESC LIMIT 1000".format(p.id))
    quotes = []
    for i in cur.fetchall():
        quotes.append(ProductQuote(i[0], i[1], i[2], i[3]))
    quotes.reverse()
    week_rets = [get_weekly_return(quotes, w) for w in weeks]
    print("last week return: {:.2f}%".format(week_rets[len(weeks) - 1] * 100))
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
    quantile = [0.05, 0.15, 0.35, 0.65, 0.85, 0.95]
    idx = 0
    total = 0
    for i in range(0, len(weeks) - 1):
        total += weighted_ret[i][1]
        if total >= quantile[idx]:
            print("{:.2f}% quantile: {:.2f}%".format(
                quantile[idx] * 100, (weighted_ret[i][0] + weighted_ret[i - 1][0]) * 50))
            idx = idx + 1
        if idx == len(quantile):
            break
