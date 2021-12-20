import json
import requests

from config import exchanger

class ConverterException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise ConverterException("Количество параметров неверное!")
        quote, base, amount = values

        if quote == base:
            raise ConverterException(f'К сожалению перевод в одинаковые валюты невозможен {base}')

        try:
            quote_formatted = exchanger[quote]
        except KeyError:
            raise ConverterException(f'Введена неизвестьная валюта {quote}')

        try:
            base_formatted = exchanger[base]
        except KeyError:
            raise ConverterException(f'Введена неизвестная валюта {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConverterException(f'Предлогаемое количество переводивой валюты не удалось обработать {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_formatted}&tsyms={base_formatted}')

        result = float(json.loads(r.content)[base_formatted])*amount

        return round(result, 3)


