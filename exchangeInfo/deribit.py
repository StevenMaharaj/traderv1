import requests
from typing import Mapping

def get_exchange_info(is_live: bool) -> Mapping[str, dict]:
        if is_live:
            base = 'https://www.deribit.com/api/v2/'
        else:
            base = "https://test.deribit.com/api/v2/"

        response_btc = requests.get(
            f'{base}public/get_instruments?currency=BTC&kind=future')
        response_eth = requests.get(
            f'{base}public/get_instruments?currency=ETH&kind=future')

        exchange_info: Mapping[str, dict] = {}
        for response in [response_btc, response_eth]:
            response_dict = response.json()
            for el in response_dict['result']:
                exchange_info[el['instrument_name']] = el

        # self.exchange_info = exchange_info
        return exchange_info