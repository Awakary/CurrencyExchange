class CurrencyDtoCreate:

    def __init__(self, code, name, sign):
        self.code = code
        self.name = name
        self.sign = sign


class CurrencyDtoList:

    def __init__(self, id,  code, name, sign):
        self.id = id
        self.code = code
        self.name = name
        self.sign = sign


class ExchangeRateDtoCreate:

    def __init__(self, baseCurrencyCode, targetCurrencyCode, rate):
        self.base_currency = baseCurrencyCode
        self.target_currency = targetCurrencyCode
        self.rate = rate


class ExchangeRateDtoList:

    def __init__(self, id,  base_currency, target_currency, rate):
        self.id = id
        self.baseCurrency = base_currency
        self.targetCurrency = target_currency
        self.rate = rate


class ExchangeRateDtoConvert:

    def __init__(self, baseCurrency, targetCurrency, rate, amount, convertedAmount):
        self.baseCurrency = baseCurrency
        self.targetCurrency = targetCurrency
        self.rate = rate
        self.amount = amount
        self.convertedAmount = convertedAmount
