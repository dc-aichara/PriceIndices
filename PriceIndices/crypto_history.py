import requests
import pandas as pd
from datetime import datetime
from typing import Any, Optional
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import warnings

warnings.filterwarnings("ignore")


class MarketHistory(object):
    __Crypto_Market_Base_URL = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?convert=USD&slug="

    def __init__(self,
                 base_url: Optional[str] = __Crypto_Market_Base_URL) -> None:
        self.base_url = base_url
        self.request_timeout = 120

        self.session = requests.Session()
        retries = Retry(
            total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504]
        )
        self.session.mount("http://", HTTPAdapter(max_retries=retries))

    def __request(self, url: str) -> pd.DataFrame:
        try:
            response = self.session.get(url, timeout=self.request_timeout)
            response.raise_for_status()
            content = response.json()

            d = content["data"]["quotes"]
            df = pd.DataFrame([v["quote"]["USD"] for v in d])
            df.sort_values("timestamp", ascending=False, inplace=True)
            df.reset_index(drop=True, inplace=True)
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df["date"] = df["timestamp"].apply(lambda x: x.strftime("%Y-%m-%d"))

            del df["timestamp"]
            return df
        except Exception as e:
            raise

    def get_history(
            self, coin_id: str, start_date: str, end_date: str
    ) -> Optional[pd.DataFrame]:
        """
        Get historical market data of a cryptocurrency from CoinMarketCap.
        Args:
            coin_id (str): coin name. E.g., bitcoin
            start_date (str): Starting date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format
        Returns:
            pd.DataFrame: Pandas Dataframe or print error message

        """
        url = "{0}{1}&time_end={2}&time_start={3}".format(
            self.base_url, coin_id, end_date, start_date
        )

        try:
            return self.__request(url)
        except Exception as e:
            print(e)
            print(
                'Please, check inputs. Coin id, and dates are strings. Date '
                'format is "YYYY-MM-DD"'
            )

    def get_price(self, coin_id: str, start_date: str, end_date: str) -> \
            Optional[pd.DataFrame]:
        """
        Get historical market price data (closing price) of a cryptocurrency
        from CoinMarketCap.
        Args:
            coin_id (str): coin name
            start_date (str): Starting date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format

        Returns:
            pd.DataFrame: Pandas Dataframe or print error message

        """
        url = "{0}{1}&time_end={2}&time_start={3}".format(
            self.base_url, coin_id, end_date, start_date
        )

        try:
            df = self.__request(url)
            df = df[["date", "close"]]
            df.columns = ["date", "price"]
            return df
        except Exception as e:
            print(
                e,
                'Please, check inputs Coin id, and dates are strings. Date '
                'format is "YYYY-MM-DD"',
            )
