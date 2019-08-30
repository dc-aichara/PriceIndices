import requests
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class MarketHistory:
    __Crypto_Market_Base_URL = 'https://coinmarketcap.com/currencies/'

    def __init__(self, price_url=__Crypto_Market_Base_URL):
        self.price_url = price_url
        self.request_timeout = 120

        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))

    def __request(self, url):
        try:
            response = self.session.get(url, timeout = self.request_timeout)
            response.raise_for_status()
            data = pd.read_html(response.content)
            df = pd.DataFrame(data[0])
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        except Exception as e:
            raise

    def get_history(self, coin_id, start_date, end_date):
        """
        Get historical market data of a cryptocurrency from CoinMarketCap.

        :param coin_id: coin name [str]
        :param start_date:  date in 'YYYYMMDD' format [str]
        :param end_date: date in 'YYYYMMDD' format [str]
        :return: Pandas DataFrame
        """
        url = '{0}{1}/historical-data/?start={2}&end={3}'.format(self.price_url, coin_id, start_date, end_date)

        try:
            return self.__request(url)
        except Exception as e:
            print(e)
            print('Please, check inputs. Coin id, and dates are strings. Date format is "YYYYMMDD"')

    def get_price(self, coin_id, start_date, end_date):
        """
          Get historical market price data (closing price) of a cryptocurrency from CoinMarketCap.
          :param coin_id: coin name [str]
          :param start_date:  date in 'YYYYMMDD' format [str]
          :param end_date: date in 'YYYYMMDD' format [str]
          :return: Pandas DataFrame
          """
        url = '{0}{1}/historical-data/?start={2}&end={3}'.format(self.price_url, coin_id, start_date, end_date)

        try:
            df = self.__request(url)
            df = df[['Date', 'Close**']]
            df.columns = ['date', 'price']
            return df
        except Exception as e:
            print(e, 'Please, check inputs Coin id, and dates are strings. Date format is "YYYYMMDD"')

