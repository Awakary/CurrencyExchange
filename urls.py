import re

from dao import CurrencyDao, ExchangeRateDao


class Url:

    def __init__(self, path):
        self.path = path

    def get_method(self):
        if re.match('/currency/', self.path):
            cur = self.path.split('/')[2]
            return CurrencyDao().list(one=cur)
        if re.match('/currencies', self.path):
            return CurrencyDao().list()
        if re.match('/exchangeRate/', self.path):
            curs = self.path.split('/')[2]
            cur1, cur2 = curs[:3], curs[3:]
            return ExchangeRateDao().list(one=cur1, two=cur2)
        if re.match('/exchangeRates', self.path):
            return ExchangeRateDao().list()

