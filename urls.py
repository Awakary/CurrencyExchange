import re
from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs
from dao import CurrencyDao, ExchangeRateDao
from dto import ExchangeRateDtoCreate, CurrencyDtoCreate
from error import Error
from service import Service


@dataclass
class Url:
    path: str
    method: str

    def choose_dao(self, data=None):
        curs = self.path.split('/')[-1]
        cur1 = curs[:3]
        cur2 = curs[3:] if len(curs) == 6 else None
        if self.method == "GET":
            if re.match('/currencies', self.path):
                return CurrencyDao().list()
            elif re.match('/exchangeRates', self.path):
                return ExchangeRateDao().list()
            elif re.match('/exchangeRate/', self.path):
                return ExchangeRateDao().list(one=cur1, two=cur2)
            elif re.match('/currency/', self.path):
                if not cur1:
                    return Error(code=400, message='Код валюты отсутствует в адресе')
                return CurrencyDao().list(one=cur1)
            elif re.match('/exchange', self.path):
                attrs = self.parse_url()
                return Service(attrs).get_exchange()
        params = parse_qs(data)
        if self.method == "POST":
            if re.match('/currencies', self.path):
                new_currency = CurrencyDtoCreate(**{key: value[0] for key, value in params.items()})
                return CurrencyDao().create(new_currency)
            if re.match('/exchangeRates', self.path):
                new_rate = ExchangeRateDtoCreate(**{key: value[0] for key, value in params.items()})
                return ExchangeRateDao().create(new_rate)
        elif self.method == "PATCH":
            if re.match('/exchangeRate/', self.path):
                return ExchangeRateDao().update(params, cur1, cur2)

    def parse_url(self):
        result = urlparse(self.path)
        return parse_qs(result.query)









    # def get_create(self, params):
    #     try:
    #
    #     except:
    #         return Error(code=400, message='Отсутствует нужное поле формы')
    #
    # def get_update(self, params, cur1, cur2):
    #     try:

    #     except:
    #         return Error(code=400, message='Отсутствует нужное поле формы')

    # def get_list(self)


    #
    # def router_for_get(self):
    #     if re.match('/currency/', self.path):
    #         cur = self.path.split('/')[2]
    #         return CurrencyDao().list(one=cur)
    #     if re.match('/currencies', self.path):
    #         return CurrencyDao().list()
    #     if re.match('/exchangeRate/', self.path):
    #         curs = self.path.split('/')[2]
    #         cur1, cur2 = curs[:3], curs[3:]
    #         return ExchangeRateDao().list(one=cur1, two=cur2)
    #     if re.match('/exchangeRates', self.path):
    #         return ExchangeRateDao().list()
    #
    # def router_for_post(self, data):
    #     params = parse_qs(data)
    #     if re.match('/currencies', self.path):
    #         return CurrencyDao().create(params)
    #     if re.match('/exchangeRates', self.path):
    #         return ExchangeRateDao().create(params)
    #
    # def router_for_patch(self, data):
    #     params = parse_qs(data)
    #     curs = self.path.split('/')[2]
    #     cur1, cur2 = curs[:3], curs[3:]
    #     if re.match('/exchangeRate/', self.path):
    #         return ExchangeRateDao().update(params, cur1, cur2)


