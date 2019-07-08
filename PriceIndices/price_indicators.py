import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import warnings
warnings.filterwarnings('ignore')


class Indices(object):

    def __abs__(self):

    def get_bvol_index(self,  price_data):

        """
         Volatility Index is a measure of market's expectation of volatility over the near term.
         Volatility is often described as the "rate and magnitude of changes in prices" and in
          finance often referred to as risk.
          Reference: www.moneycontrol.com

          Calculate Cryptocureency price's 30 days volatile index
          :param price_data: pandas DataFrame
          :return: pandas DataFrame
          """
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
            return e

    def get_bvol_graph(self, bvol_data):

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
            plt.savefig('bvol_index.png')
            return plt.show()
        except Exception as e:
            return  e

    def get_rsi(self, price_data):

        """
        Type:
            Momentum indicator

        Computation:
                    It is based on the average price increase during a period of rising prices and average price fall
                    during a period of falling stock prices. Relative Strength Index (RSI) is plotted between 0 and 100.

        What it signals
                        Usually, the market is treated as overbought when RSI goes above 70 (80 for highly volatile
                         stocks) and oversold when it hits 30—20 for highly volatile stocks.

        Reference:
                    https://economictimes.indiatimes.com/
        :param price_data: pandas DataFrame

        :return: pandas DataFrame
        """
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
            return e

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
            plt.text('2019-06-01', 71.5, '>70 OverBought', fontsize=20, color='green')
            plt.text('2019-06-01', 23, '<30 OverSold', fontsize=20, color='green')
            plt.legend()
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=90)
            ax2.xaxis.set_major_locator(ticker.MultipleLocator(30))

            ax2.tick_params(axis='x', colors='b')
            ax2.tick_params(axis='y', colors='b')

            ax2.axhline(y=70, color='r')
            ax2.axhline(y=30, color='r')

            plt.suptitle('Price  and  Relative  Strength Index', color='red', fontsize=24)
            plt.save('rsi.png')
            return plot.show()
        except Exception as e:
            return e

    def get_bollinger_bands(self, price_data, days=20):
        """
        Type:
            Trend, volatility, momentum indicator

        Computation:
                    They comprise three lines: A 20-day moving average, an upper band and lower band—the upper and
                     lower bands are plotted as two standard deviations from the moving average.

        What it signals:
                        The moving average shows the trend, the gap between upper and lower band
                        shows volatility in the counter.

        Reference:
                    https://economictimes.indiatimes.com/
                    https://www.bollingerbands.com/bollinger-bands
        :param days: int
        :param price_data: pandas DataFrame
        :return: a pandas DataFrame and save a plot to local project directory as 'bollinger_bands.png'.
        """

        try:
            df = price_data
            df['SMA'] = df['price'].rolling(days).mean()
            df['SD'] = df['price'].rolling(days).std()
            df['pluse'] = df['SMA'] + df['SD']*2
            df['minus'] = df['SMA'] - df['SMA']*2

            fig, ax = plt.subplots(figsize=(20, 16))
            plt.plot(df['date'], df['pluse'], color='g')
            plt.plot(df['date'], df['minus'], color='g')
            plt.plot(df['date'], df['price'], color='orange')
            plt.legend()
            plt.xlabel('Time', color ='b', fontsize =22)
            plt.ylabel('Price', color ='b', fontsize =22)
            plt.title('Bollinger Bands', color ='b', fontsize =27)
            plt.tick_params(labelsize =17)
            fig.set_facecolor('yellow')
            plt.grid()
            plt.savefig('bollinger_bands.png', bbox_inches='tight', facecolor='yellow')
            plt.show()
            return df
        except Exception as e:
            return e

    def moving_average_convergence_divergence(self, price_data):
        """
        Type
            Trend and momentum indicator

        Computation
            The difference between 12 and 26-day moving averages.

        What it signals
            Rising Moving Average Convergence Divergence (MACD) indicates an upward price trend
             and falling MACD indicates a downward price trend.

        Reference:
            https://economictimes.indiatimes.com/
        :param price_data: pandas DataFrame
        :return:
        """



    def simple_moving_average(self, price_data, days):
        """
        Simple moving average of given days
        :param price_data: pandas DataFrame
        :param days: int
        :return: pandas DataFrame
        """
        try:
            df = price_data
            df['SMA'] = df['price'].rolling(days).mean()
            return df
        except Exception as e:
            return print('SMA Error - {}'.format(e))




