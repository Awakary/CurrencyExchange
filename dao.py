import json
import sqlite3
from abc import ABC
from sqlite3 import Cursor
from urllib.parse import urlparse, parse_qs
from models import Currency, ExchangeRate
from views import View


class BaseDao:

    def __init__(self, table, model):
        self.table = table
        self.model = model

    def connect_to_db(self, sql: str) -> Cursor:
        connection = sqlite3.connect('DB.sqlite')
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor
    # def create(self, request, data):
    #     new_object = self.model(**data)
    #     sql = "INSERT INTO {self.table}"
    #     cursor = self.connect_to_db(sql)


class CurrencyDao(BaseDao):

    def __init__(self):
        super().__init__('Currencies', Currency)

    def list(self, one: str = None) -> json:
        if one:
            sql = f"SELECT * FROM {self.table} WHERE code='{one.lower()}'"
        else:
            sql = f"SELECT * FROM {self.table}"
        cursor = self.connect_to_db(sql)
        result = cursor.fetchall()
        return result, cursor.description


class ExchangeRateDao(BaseDao):

    def __init__(self):
        super().__init__('ExchangeRates', ExchangeRate)

    def list(self, one: str = None, two: str = None) -> json:
        if one and two:
            sql = f""" SELECT * FROM {self.table} WHERE 
                  base_currency = (SELECT id FROM Currencies WHERE code='{one.lower()}') and 
                  target_currency = (SELECT id FROM Currencies WHERE code='{two.lower()}')
                  UNION
                  SELECT * FROM Currencies WHERE code in ('{one.lower()}', '{two.lower()}')"""
        else:
            sql = f"""SELECT * FROM {self.table}
            UNION
            SELECT * FROM Currencies WHERE id in (SELECT base_currency FROM {self.table})
            UNION
            SELECT * FROM Currencies WHERE id in (SELECT target_currency FROM {self.table})
            """
        cursor = self.connect_to_db(sql)
        result = cursor.fetchall()
        return result, cursor.description




