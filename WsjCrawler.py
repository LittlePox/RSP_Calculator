from Crawler import Crawler
from ProductQuote import ProductQuote
from datetime import timedelta
from Product import Product

class WsjCrawler(Crawler):
    def crawl_by_dates(self, product, start, end):
        res = []
        i = start
        while i <= end:
            res.append(ProductQuote(0, str(i), 0, 0))
            i = i + timedelta(days=1)
        return res