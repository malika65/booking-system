import requests
from django.conf import settings


class CurrencyExchangeService:

    @staticmethod
    def get_rates_from_api(currency_to, currency_from, amount):
        headers = {'content-type': 'application/json', 'apikey': f'{settings.CURRENCY_RATES_API_KEY}'}
        url = f'{settings.CURRENCY_RATES_URL}/convert?to={currency_to}&from={currency_from}&amount={amount}'
        return requests.get(url, headers=headers).json()
