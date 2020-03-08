from Crawler import Crawler
from ProductQuote import ProductQuote
from datetime import timedelta
from Product import Product
import os
import os.path


class WsjCrawler(Crawler):
    def crawl_by_dates(self, product, start, end):
        url = r"'https://www.wsj.com/market-data/quotes/index/XX/000300/historical-prices/download?MOD_VIEW=page&num_rows=90&range_days=90&startDate=12/09/2019&endDate=03/08/2020'"
        output = self.current_dir + "/prices.csv"
        for i in range(0, 10):
            print('trial ' + str(i))
            if os.path.exists(output) and os.stat(output).st_size > 0:
                os.remove(output)
                break
            os.system(' '.join(
                ['wget', url, '-e use_proxy=yes -e https_proxy=127.0.0.1:7890', "-O '" + output + "'"]))
