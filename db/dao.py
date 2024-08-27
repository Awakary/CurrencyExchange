import sqlite3
from sqlite3 import Cursor

from settings.settings import database
from utils.dto import CurrencyDtoCreate, CurrencyDtoList, ExchangeRateDtoCreate
from utils.error import Error
from utils.utils import converter_rates_to_dto


class BaseDao:
    """Класс работы с базой данных"""

    @staticmethod
    def connect_to_db(sql: str, fields: tuple = ()) -> Cursor | Error:
        """Функция подключения к базе данных"""

        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, fields)
            connection.commit()
            return cursor


class CurrencyDao(BaseDao):

    def list(self, one: str = None) -> list | Error:

        """Функция получения валют"""

        try:
            if one:
                sql = """SELECT * FROM Currencies WHERE code=?"""
                cursor = self.connect_to_db(sql, (one,))
            else:
                sql = """SELECT * FROM Currencies"""
                cursor = self.connect_to_db(sql)
        except sqlite3.OperationalError:
            return Error(code=500, message='База данных недоступна')
        result = cursor.fetchall()
        if one and not result:
            return Error(code=404, message='Валюта не найдена')
        dto_list = [CurrencyDtoList(*line) for line in result]
        return dto_list

    def create(self, new_currency: CurrencyDtoCreate) -> list:

        """Функция создания валюты"""

        sql = """INSERT INTO Currencies (name, code, sign)
                 VALUES (?, ?, ?)"""
        try:
            self.connect_to_db(sql, (new_currency.name, new_currency.code, new_currency.sign))
        except sqlite3.IntegrityError:
            return Error(code=409, message='Валюта с таким кодом уже существует')
        except sqlite3.OperationalError:
            return Error(code=500, message='База данных недоступна')
        return self.list(one=new_currency.code)


class ExchangeRateDao(BaseDao):

    def list(self, one: str | int = None, two: str | int = None) -> list | Error:

        """Функция получения курсов"""

        try:
            if one and two:
                sql = """ SELECT * FROM ExchangeRates WHERE 
                base_currency = (SELECT id FROM Currencies WHERE code= ?)
                and target_currency = (SELECT id FROM Currencies WHERE code= ?)
                UNION
                SELECT * FROM Currencies WHERE code in (?, ?)"""
                cursor = self.connect_to_db(sql, (one, two, one, two))
            else:
                sql = """SELECT * FROM ExchangeRates
                UNION
                SELECT * FROM Currencies WHERE id in (SELECT base_currency FROM ExchangeRates)
                UNION
                SELECT * FROM Currencies WHERE id in (SELECT target_currency FROM ExchangeRates)
                """
                cursor = self.connect_to_db(sql)
        except sqlite3.OperationalError:
            return Error(code=500, message='База данных недоступна')
        result = cursor.fetchall()
        if len(result) < 3:
            return Error(code=404, message='Обменный курс для пары не найден')
        dto_list_rates = converter_rates_to_dto(result)
        return dto_list_rates

    def create(self, new_rate: ExchangeRateDtoCreate) -> list:

        """Функция создания курса"""

        sql = """INSERT INTO ExchangeRates (base_currency, target_currency, rate)
              VALUES ((SELECT id FROM Currencies WHERE code = ?), 
              (SELECT id FROM Currencies WHERE code = ?), 
              ?)"""
        try:
            self.connect_to_db(sql, (new_rate.base_currency, new_rate.target_currency, new_rate.rate))
        except sqlite3.IntegrityError:
            return Error(code=409, message='Валютная пара с таким кодом уже существует')
        except sqlite3.OperationalError:
            return Error(code=500, message='База данных недоступна')
        return self.list(one=new_rate.base_currency, two=new_rate.target_currency)

    def update(self, params, one: str | int, two: str | int) -> list:

        """Функция обновления курса"""

        new_rate = params.get('rate')[0]
        sql = """UPDATE ExchangeRates SET rate =  ?
            WHERE base_currency = (SELECT id FROM Currencies WHERE code=?)
            AND target_currency = (SELECT id FROM Currencies WHERE code=?)"""
        try:
            self.connect_to_db(sql, (new_rate, one, two))
        except sqlite3.OperationalError:
            return Error(code=500, message='База данных недоступна')
        return self.list(one=one, two=two)
