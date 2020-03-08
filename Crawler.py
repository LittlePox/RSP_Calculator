from datetime import date, timedelta
from Product import Product
from abc import ABC, abstractmethod
import pathlib


class Crawler:
    current_dir = str(pathlib.Path(__file__).parent.absolute())

    @abstractmethod
    def crawl_by_dates(self, product, start, end):
        pass

    def crawl(self, product):
        end = date.today()
        start = end - timedelta(days=10)
        return self.crawl_by_dates(product, start, end)
