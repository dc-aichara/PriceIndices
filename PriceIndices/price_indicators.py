import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


class Indices:
    def get_bvol_index(df):

        """
         Volatility Index is a measure of market's expectation of volatility over the near term.
         Volatility is often described as the "rate and magnitude of changes in prices" and in
          finance often referred to as risk.
          Reference: www.moneycontrol.com

          Calculate Cryptocureency price's 30 days volatile index
          :param data: Pandas DataFrame with price column
          :return: pandas DataFrame
          """

        try:
            data = df
            data.columns = ['date', 'price']
            data = data.sort_values(by='date').reset_index(drop=True)
            ln_ratio_btc = pd.DataFrame(list(np.diff(np.log(data['price']))))
            bvol_btc = pd.DataFrame(ln_ratio_btc.rolling(30).std() * np.sqrt(365))
            bvol_btc.columns = ['BVOL_Index']
            data1 = pd.concat([data, bvol_btc], join='inner', axis=1)
            data1 = data1.dropna()
            data1 = data1.sort_values(by='date', ascending=False).reset_index(drop=True)
            return data1
        except Exception as e:
            return e

    def get_bvol_graph(df):

        """Make a line graph of bvol index with respect to time"""
        try:
            data = df
            fig, ax = plt.subplots(figsize=(14, 12))
            rect = fig.patch
            rect.set_facecolor('yellow')
            ax1 = plt.subplot(211)
            ax1.plot(data['date'], data['price'], color='blue', label='Price')
            plt.ylabel('Price', color='red', fontsize=20)
            ax1.axes.get_xaxis().set_ticks([])
            plt.legend()
            ax1.tick_params(axis='y', colors='b')
            ax1.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

            ax2 = plt.subplot(212)
            ax2.plot(data['date'], data['BVOL_Index'], color='b', label='BVOL Index')
            plt.xlabel('Time', color='red', fontsize=20)
            plt.ylabel('Volatility Index', color='r', fontsize=20)
            plt.legend()
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=90)
            ax2.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

            ax2.tick_params(axis='x', colors='b')
            ax2.tick_params(axis='y', colors='b')

            plt.suptitle('Price  and  Volatility Index', color='red', fontsize=24)
            plt.savefig('bvol_index.png', bbox_inches='tight', facecolor='orange')
            return plt.show()
        except Exception as e:
            return e

    def get_rsi(df):

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
        :param price_data: Pandas DataFrame with price column

        :return: pandas DataFrame
        """
        try:
            data = df
            data['price_change'] = data['price'] - df['price'].shift(1)
            data.dropna(inplace=True)
            data['gain'] = data['price_change'].apply(lambda x: x if x >= 0 else 0)

            data['loss'] = data['price_change'].apply(lambda x: abs(x) if x <= 0 else 0)

            data['gain_average'] = data['gain'].rolling(14).mean()

            data['loss_average'] = data['loss'].rolling(14).mean()

            data['RS'] = data['gain_average'] / df['loss_average']

            data['RSI_1'] = 100 * (1 - (1 / (1 + df['RS'])))

            data['RS_Smooth'] = (data['gain_average'].shift(1) * 13 + df['gain']) / (
                        data['loss_average'].shift(1) * 13 + data['loss'])

            data['RSI_2'] = 100 * (1 - (1 / (1 + data['RS_Smooth'])))
            data = data.fillna(0).reset_index(drop=True)
            data1 = data
            return data1
        except Exception as e:
            return e

    def get_rsi_graph(self, rsi_data):
        try:
            df = rsi_data
            fig, ax = plt.subplots(figsize=(14, 12))
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
            plt.text(df['date'][int(len(df)/2)], 80, '>70 OverBought', fontsize=20, color='black')
            plt.text(df['date'][int(len(df)/2)], 15, '<30 OverSold', fontsize=20, color='black')
            plt.legend()
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=90)

            ax2.tick_params(axis='x', colors='b')
            ax2.tick_params(axis='y', colors='b')

            ax2.axhline(y=70, color='r')
            ax2.axhline(y=30, color='r')

            plt.suptitle('Price  and  Relative  Strength Index', color='red', fontsize=24)
            plt.savefig('rsi.png', bbox_inches='tight', facecolor='orange')
            return plt.show()
        except Exception as e:
            return e

    def get_bollinger_bands(df, days=20):
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
        :param price_data: Pandas DataFrame with price column
        :return: a pandas DataFrame and save a plot to local project directory as 'bollinger_bands.png'.
        """

        try:
            data = df
            data['SMA'] = data['price'].rolling(days).mean()
            data['SD'] = data['price'].rolling(days).std()
            data['pluse'] = data['SMA'] + data['SD']*2
            data['minus'] = data['SMA'] - data['SMA']*2
            data1 = data
            fig, ax = plt.subplots(figsize=(16, 12))
            plt.plot(data1['date'], data1['pluse'], color='g')
            plt.plot(data1['date'], data1['minus'], color='g')
            plt.plot(data1['date'], data1['price'], color='orange')
            plt.legend()
            plt.xlabel('Time', color='b', fontsize=22)
            plt.ylabel('Price', color='b', fontsize=22)
            plt.title('Bollinger Bands', color='b', fontsize=27)
            plt.tick_params(labelsize=17)
            fig.set_facecolor('yellow')
            plt.grid()
            plt.savefig('bollinger_bands.png', bbox_inches='tight', facecolor='orange')
            plt.show()
            return data1
        except Exception as e:
            return e

    def get_moving_average_convergence_divergence(df):
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
        :param price_data: Pandas DataFrame with price column
        :return: pandas DataFrame
        """
        try:
            data = df
            data['EMA_12'] = data['price'].ewm(span=12, adjust=False).mean()
            data['EMA_26'] = data['price'].ewm(span=26, adjust=False).mean()
            data['MACD'] = data['EMA_12'] - data['EMA_26']
            data1 = data.dropna()

            fig, ax = plt.subplots(figsize=(14, 9))
            plt.plot(data1['date'], data1['price'], color='r', label='Price')
            plt.plot(data1['date'], data1['MACD'], color='b', label='MACD')
            plt.legend()
            plt.title('Price and MACD Plot', fontsize=28, color='b')
            plt.xlabel('Time', color='b', fontsize=19)
            plt.ylabel('Price', color='b', fontsize=19)
            plt.savefig('macd.png', bbox_inches='tight', facecolor='orange')
            fig.set_facecolor('orange')
            plt.show()

            return data1
        except Exception as e:
            return print('MACD Error - {}'.format(e))

    def get_simple_moving_average(df, days=15):
        """
        Simple moving average of given days
        :param price_data: pandas DataFrame
        :param days: int
        :return: pandas DataFrame
        """
        try:
            data = df
            data['SMA'] = data['price'].rolling(days).mean()
            data1 = data.dropna()
            fig, ax = plt.subplots(figsize=(14, 9))
            plt.plot(data1['date'], data1['price'], color='r', label='Price')
            plt.plot(data1['date'], data1['SMA'], color='b', label='SMA')
            plt.legend()
            plt.title('Price and SMA Plot', fontsize=28, color='b')
            plt.xlabel('Time', color='b', fontsize=19)
            plt.ylabel('Price', color='b', fontsize=19)
            plt.savefig('sma.png', bbox_inches='tight', facecolor='orange')
            fig.set_facecolor('orange')
            plt.show()
            return data1
        except Exception as e:
            return print('SMA Error - {}'.format(e))

    def get_exponential_moving_average(df, periods=[20]):
        """
        The EMA is a moving average that places a greater weight and significance on the most recent data points.
        Like all moving averages, this technical indicator is used to produce buy and sell signals based on crossovers and divergences from the historical average.
        Traders often use several different EMA days, for instance, 20-day, 30-day, 90-day, and 200-day moving averages.
        Reference: https://www.investopedia.com/
        :param price_data: Pandas DataFrame with price column
        :param period: a list of periods (int)
        :return:
        """
        try:
            data = df
            for period in periods:
                data['EMA_{}'.format(period)] = data['price'].ewm(span=period, adjust=False).mean()
                data = data.dropna()
            data1 = data
            fig, ax = plt.subplots(figsize=(14, 9))
            plt.plot(data1['date'], data1['price'], color='r', label='Price')
            for period in periods:
                plt.plot(data1['date'], data1['EMA_{}'.format(period)], label='EMA_{}'.format(period))
            plt.legend()
            plt.title('Price and EMA Plot', fontsize=28, color='b')
            plt.xlabel('Time', color='b', fontsize=19)
            plt.ylabel('Price/EMA', color='b', fontsize=19)
            plt.savefig('ema.png', bbox_inches='tight', facecolor='orange')
            fig.set_facecolor('orange')
            plt.show()
            return data1
        except Exception as e:
            return print('EMA Error - {}'.format(e))

