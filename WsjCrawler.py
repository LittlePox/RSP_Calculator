from Crawler import Crawler
from ProductQuote import ProductQuote
from datetime import timedelta
from Product import Product
from urllib import request
from datetime import datetime
import time
import gzip


class WsjCrawler(Crawler):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'datadome=ALF~4vb~~onXyPspObRkELbvlhRydeqfShsemWLIAp_hcQjQU_ILmvhAbabVo2imC0HxDG4ePOZjhTpl0Uqm31a_Vgz3ObgXOvRgLXzzgWfEUQI8jy1nYhFQOY_55SBd',
        'Priority': 'u=0, i',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

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
                req = request.Request(url, headers=WsjCrawler.headers)
                content = request.urlopen(req)
                if content.info().get('Content-Encoding') == 'gzip':
                    # Decompress the gzip content
                    with gzip.GzipFile(fileobj=content) as gzip_response:
                        url_content = gzip_response.read().decode('UTF-8')
                else:
                    url_content = content.read().decode('UTF-8')
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
