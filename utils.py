from dto import ExchangeRateDtoList, CurrencyDtoList


def converter_currency_for_rate(dto_list_currencies: list, rate: dict) -> dict:
    currencies_dict = {'baseCurrency': '', 'targetCurrency': ''}
    for j in dto_list_currencies:
        if j['id'] == rate['baseCurrency']:
            currencies_dict['baseCurrency'] = j
        if j['id'] == rate['targetCurrency']:
            currencies_dict['targetCurrency'] = j
    return currencies_dict


def converter_rates_to_dto(result):
    dto_list_currencies = []
    dto_list_rates = []
    for line in result:
        if all([(isinstance(j, int | float)) for j in line]):
            dto_list_rates.append(ExchangeRateDtoList(*line).__dict__)
        else:
            dto_list_currencies.append(CurrencyDtoList(*line).__dict__)
    for rate in dto_list_rates:
        currencies_dict = converter_currency_for_rate(dto_list_currencies, rate)
        rate['baseCurrency'] = currencies_dict['baseCurrency']
        rate['targetCurrency'] = currencies_dict['targetCurrency']
    return dto_list_rates
