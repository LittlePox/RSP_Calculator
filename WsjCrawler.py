from Crawler import Crawler
from ProductQuote import ProductQuote
from datetime import timedelta
from Product import Product
from urllib import request
from datetime import datetime
import time


class WsjCrawler(Crawler):
    def crawl_by_dates(self, product, start, end):
        str_start = start.strftime('%m/%d/%Y')
        str_end = end.strftime('%m/%d/%Y')
        url = r'https://www.wsj.com/market-data/quotes/{0}/historical-prices/download?MOD_VIEW=page&num_rows=10000&range_days=10000&startDate={1}&endDate={2}'.format(
            product.wsjTicker, str_start, str_end
        )
        print('Crawling {0}...'.format(url))

        #proxy = request.ProxyHandler({'https': '127.0.0.1:7890'})
        #opener = request.build_opener(proxy)
        #request.install_opener(opener)

        for i in range(0, 5):
            print('trial {0}'.format(i))
            try:
                req = request.Request(url, headers={
                                      'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0", 'Referer': url})
                url_content = request.urlopen(
                    req, timeout=20).read().decode('UTF-8')
                lines = url_content.splitlines()[1:]
                res = []
                for line in lines:
                    res.append(self.convert_to_quote(product, line))
                return res
            except Exception as e:
                print(e)
                time.sleep(3 * (i + 1))
        return []

    def convert_to_quote(self, product, line):
        cells = line.split(', ')
        cob_date = datetime.strptime(cells[0], '%m/%d/%y').date()
        close = float(cells[4])
        nav = close
        return ProductQuote(product.id, cob_date, close, nav)
