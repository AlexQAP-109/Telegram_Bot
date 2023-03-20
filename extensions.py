import json
import requests
from config import slovar


class APIException(Exception):
    pass

class ConverterPrice:
    def get_price(quote:str, base:str,amount:str):

        if quote == base:
            raise APIException(f'Не допустимый обмен {quote} на {base}')

        try:
            znachenie_quote = slovar[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            znachenie_base = slovar[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удается обработать колличество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={znachenie_quote}&tsyms={znachenie_base}')
        a = json.loads(r.content)[znachenie_base]
        return a
