from urllib.parse import parse_qs, urlparse

from db.dao import CurrencyDao, ExchangeRateDao
from service import Service
from utils.error import Error
from utils.utils import converter_to_create_dto


class Router:

    """Класс маршрутизации"""

    def __init__(self, path: str, method: str, data: str):
        self.path = path
        self.method = method
        self.cur1, self.cur2 = self.get_curs()
        self.params = parse_qs(data)
        self.all_paths = self.get_all_paths()

    def get_router(self):

        """Функция получения маршрута"""

        router = self.all_paths[self.method][self.get_path_key()]
        if hasattr(router, '__call__'):
            try:
                return router()
            except (TypeError, KeyError):
                return Error(code=400, message='Отсутствует нужное поле формы')
        return router

    def get_all_paths(self) -> dict:

        """Функция получения всех доступных маршрутов"""

        return {'GET': {'currencies': CurrencyDao().list(),
                        'exchangeRates': ExchangeRateDao().list(),
                        'exchangeRate': ExchangeRateDao().list(one=self.cur1, two=self.cur2),
                        'currency': CurrencyDao().list(one=self.cur1),
                        'exchange': lambda: Service(self.parse_url()).get_exchange()},
                'POST': {'currencies': lambda: CurrencyDao().create(converter_to_create_dto(self.params)),
                         'exchangeRates': lambda: ExchangeRateDao().create(converter_to_create_dto(self.params))},
                'PATCH': {'exchangeRate': lambda: ExchangeRateDao().update(self.params, self.cur1, self.cur2)}}

    def get_path_key(self) -> str:

        """Функция обработки пути"""

        path = self.path.split('/')[1]
        if '?' in path:
            return path[:path.find('?')]
        return path

    def parse_url(self) -> dict:

        """Функция парсинга url"""

        result = urlparse(self.path)
        return parse_qs(result.query)

    def get_curs(self) -> tuple:

        """Функция получения кодов валют"""

        curs = self.path.split('/')[-1]
        cur1 = curs[:3]
        cur2 = curs[3:] if len(curs) == 6 else None
        return cur1, cur2


