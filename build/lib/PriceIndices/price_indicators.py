import requests
import pandas as pd
import numpy as np
import warnings
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
warnings.filterwarnings('ignore')


class price:
    __Crypto_Price_Base_URL = 'https://coinmarketcap.com/currencies/'

    def __init__(self, price_url=__Crypto_Price_Base_URL):
        self.price_url = price_url
        self.request_timeout = 120

        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))

    def __request(self, url):
        try:
            response = self.session.get(url, timeout = self.request_timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', {'class': 'table'})

            data = [[td.text.strip() for td in tr.findChildren('td')]
                    for tr in table.findChildren('tr')]

            df = pd.DataFrame(data)
            df = df.drop(columns=[1, 2, 3, 5, 6])
            df = df.drop(0, 0).reset_index(drop=True)
            df.columns = ['date', 'price']
            df['date'] = pd.to_datetime(df['date'])
            df['price'] = df['price'].astype(np.float)
            return df
        except Exception as e:
            raise

    def get_price(self, coin_id, start_date, end_date):

        """Get historical price data of cryptocurrency from CoinMarketCap.
         This will take cryptocurrency name, start date and end date as inputs.
         All inputs are strings. Date format is 'YYYYMMDD' """
        url = '{0}{1}/historical-data/?start={2}&end={3}'.format(self.price_url, coin_id, start_date, end_date)

        try:
            return self.__request(url)
        except Exception as e:
            print(e)

            print('Please, check inputs. Coin id, and dates are strings. Date format is "YYYYMMDD"')


class indices:

    def get_bvol_index( price_data):

        """ Calculate Cryptocureency price's 30 days volatile index """
        try:
            df = price_data
            df = df.sort_values(by='date').reset_index(drop=True)
            ln_ratio_btc = pd.DataFrame(list(np.diff(np.log(df['price']))))
            bvol_btc = pd.DataFrame(ln_ratio_btc.rolling(30).std() * np.sqrt(365))
            bvol_btc.columns = ['BVOL_Index']
            df = pd.concat([df,bvol_btc], join='inner', axis=1)
            df = df.dropna()
            df = df.sort_values(by='date', ascending=False).reset_index(drop=True)
            return df
        except Exception as e:
            print(e)

    def get_bvol_graph( bvol_data):

        """Make a line graph of bvol index with respect to time"""
        try:
            df = bvol_data
            fig, ax = plt.subplots(figsize=(16, 12))
            rect = fig.patch
            rect.set_facecolor('yellow')
            ax1 = plt.subplot(211)
            ax1.plot(df['date'], df['price'], color='blue', label='Price')
            plt.ylabel('Price', color='red', fontsize=20)
            ax1.axes.get_xaxis().set_ticks([])
            plt.legend()
            ax1.tick_params(axis='y', colors='b')
            ax1.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

            ax2 = plt.subplot(212)
            ax2.plot(df['date'], df['BVOL_Index'], color='b', label='BVOL Index')
            plt.xlabel('Time', color='red', fontsize=20)
            plt.ylabel('Volatility Index', color='r', fontsize=20)
            plt.legend()
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=90)
            ax2.xaxis.set_major_locator(ticker.MultipleLocator(30))
            ax2.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

            ax2.tick_params(axis='x', colors='b')
            ax2.tick_params(axis='y', colors='b')

            plt.suptitle('Price  and  Volatility Index', color='red', fontsize=24)

            return plt.show()
        except Exception as e:
            print(e)

    def get_rsi(price_data):

        """calculate Relative Strength Index"""
        try:
            df = price_data
            df['price_change'] = (df['price'] - df['price'].shift(1))
            df = df.dropna()
            df['gain'] = df['price_change'].apply(lambda x: x if x >= 0 else 0)

            df['loss'] = df['price_change'].apply(lambda x: abs(x) if x <= 0 else 0)

            df['gain_average'] = df['gain'].rolling(14).mean()

            df['loss_average'] = df['loss'].rolling(14).mean()

            df['RS'] = df['gain_average'] / df['loss_average']

            df['RSI_1'] = 100 * (1 - (1 / (1 + df['RS'])))

            df['RS_Smooth'] = (df['gain_average'].shift(1) * 13 + df['gain']) / (
                        df['loss_average'].shift(1) * 13 + df['loss'])

            df['RSI_2'] = 100 * (1 - (1 / (1 + df['RS_Smooth'])))
            df = df.fillna(0).reset_index(drop=True)

            return df
        except Exception as e:
            print(e)

    def get_rsi_graph(rsi_data):
        try:
            df = rsi_data
            fig, ax = plt.subplots(figsize=(16, 12))
            rect = fig.patch
            rect.set_facecolor('yellow')
            ax1 = plt.subplot(211)
            ax1.plot(df['date'], df['price'], color='blue', label='Price')
            plt.ylabel('Price ($)', color='red', fontsize=20)
            ax1.axes.get_xaxis().set_ticks([])
            plt.legend()
            ax1.tick_params(axis='y', colors='b')

            ax2 = plt.subplot(212)
            ax2.plot(df['date'], df['RSI_2'], color='b', label='RSI')
            plt.xlabel('Time', color='red', fontsize=20)
            plt.ylabel('Relative Strength Index (RSI)', color='r', fontsize=20)
            plt.text('2019-03-01', 71.5, '>70 OverBought', fontsize=20, color='green')
            plt.text('2019-03-01', 23, '<30 OverSold', fontsize=20, color='green')
            plt.legend()
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=90)
            ax2.xaxis.set_major_locator(ticker.MultipleLocator(30))

            ax2.tick_params(axis='x', colors='b')
            ax2.tick_params(axis='y', colors='b')

            ax2.axhline(y=70, color='r')
            ax2.axhline(y=30, color='r')

            plt.suptitle('Price  and  Relative  Strength Index', color='red', fontsize=24)

            return plot.show()
        except Exception as e:
            print(e)

