from Product import Product
import sqlite3
import pathlib
from WsjCrawler import WsjCrawler


cur_dir = str(pathlib.Path(__file__).parent.absolute())
conn = sqlite3.connect(cur_dir + '/database.db')
cur = conn.cursor()

cur.execute("select * from PRODUCT")
products = cur.fetchall()

crawler = WsjCrawler()
res = crawler.crawl(None)

