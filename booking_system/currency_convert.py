import requests
from django.conf import settings

from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class CurrencyExchangeService:

    @staticmethod
    def get_rates_from_api():
        if cache.get('rates'):
            return cache.get('rates')
        else:
            rates = []
            headers = {'content-type': 'application/json', 'apikey': f'{settings.CURRENCY_RATES_API_KEY}'}
            url = f'{settings.CURRENCY_RATES_URL}/latest?symbols=KGS, KZT, USD&base=USD'
            url1 = f'{settings.CURRENCY_RATES_URL}/latest?symbols=USD, KZT, KGS&base=KGS'
            url2 = f'{settings.CURRENCY_RATES_URL}/latest?symbols=USD, KGS, KZT&base=KZT'
            usd_rate = {}
            kgs_rate = {}
            kzt_rate = {}
            usd_rate['USD'] = requests.get(url, headers=headers).json()['rates']
            kgs_rate['KGS'] = requests.get(url1, headers=headers).json()['rates']
            kzt_rate['KZT'] = requests.get(url2, headers=headers).json()['rates']
            rates.append(usd_rate)
            rates.append(kgs_rate)
            rates.append(kzt_rate)
            cache.set('rates', rates, timeout=CACHE_TTL)
            return rates
