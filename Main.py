from Product import Product
import sqlite3
import pathlib
from WsjCrawler import WsjCrawler


cur_dir = str(pathlib.Path(__file__).parent.absolute())
conn = sqlite3.connect(cur_dir + '/database.db')
cur = conn.cursor()

products = []
cur.execute("select * from PRODUCT")
for i in cur.fetchall():
    products.append(Product(i[0], i[1], i[2], i[3], i[4]))

crawler = WsjCrawler()

for p in products:
    crawler.crawl(p)
