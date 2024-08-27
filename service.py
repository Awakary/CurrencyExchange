from decimal import Decimal, InvalidOperation

from db.dao import ExchangeRateDao
from utils.dto import ExchangeRateDtoConvert
from utils.error import Error


class Service:
    """Класс для конвертации валют"""

    def __init__(self, attrs: dict):
        self.base = attrs['from'][0]
        self.target = attrs['to'][0]
        self.amount = attrs['amount'][0]

    def get_exchange(self) -> ExchangeRateDtoConvert | Error | dict:

        """Функция получения метода расчета курса"""

        all_rates = ExchangeRateDao().list()
        if isinstance(all_rates, Error):
            return all_rates
        rates_dict = {(line['baseCurrency']['code'], line['targetCurrency']['code']):
        line for line in all_rates}
        try:
            line = rates_dict.get((self.base, self.target), None)
            if line:
                return self.get_normal_rate(line)
            line = rates_dict.get((self.target, self.base), None)
            if line:
                return self.get_reverse_rate(line)
            return self.get_cross_rate(all_rates)
        except InvalidOperation:
            return Error(code=400, message='Неверный формат введенных данных')

    def get_normal_rate(self, line) -> ExchangeRateDtoConvert:

        """Функция расчета обычного курса"""

        convertedAmount = (Decimal(self.amount) * Decimal(line['rate'])).quantize(Decimal("1.00"))
        line.update(amount=self.amount,
                    convertedAmount=str(convertedAmount))
        del line['id']
        return ExchangeRateDtoConvert(**line)

    def get_reverse_rate(self, line: dict) -> dict:

        """Функция расчета обратного курса"""

        convertedAmount = (Decimal(self.amount) * 1 / Decimal(line['rate'])).quantize(Decimal("1.00"))
        line.update(amount=self.amount,
                    convertedAmount=str(convertedAmount))
        del line['id']
        d = ExchangeRateDtoConvert(**line).__dict__
        d['baseCurrency'], d['targetCurrency'] = d['targetCurrency'], d['baseCurrency']
        return d

    def get_cross_rate(self, all_rates: list) -> ExchangeRateDtoConvert | Error:

        """Функция расчета кросс-курса"""

        bases = [line for line in all_rates if line['targetCurrency']['code'] == self.base]
        targets = [line for line in all_rates if line['targetCurrency']['code'] == self.target]
        for i in bases:
            for j in targets:
                if i['baseCurrency']['code'] == j['baseCurrency']['code']:
                    cross_rate = Decimal(i['rate']) / Decimal(j['rate']).quantize(Decimal("1.00"))
                    convertedAmount = (Decimal(self.amount) * cross_rate).quantize(Decimal("1.00"))
                    return ExchangeRateDtoConvert(baseCurrency=i['targetCurrency'],
                                                  targetCurrency=j['targetCurrency'],
                                                  amount=self.amount, rate=str(cross_rate),
                                                  convertedAmount=str(convertedAmount))

        return Error(code=404, message='Валютная пара отсутствует в базе данных')
