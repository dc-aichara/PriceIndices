import pandas as pd
import numpy as np
from typing import List, Optional
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")


class Indices:
    """
    Price Technical Indicators
    """

    def __init__(
        self, df: pd.DataFrame, date_col: str = "date", price_col: str = "price"
    ) -> None:
        self.df = df
        self.date_col = date_col
        self.price_col = price_col

    def get_vola_index(
        self, volatile_period: Optional[int] = 30
    ) -> pd.DataFrame:
        """
        Volatility Index is a measure of market's expectation of volatility over
        the near term.
        Volatility is often described as the "rate and magnitude of changes in
        prices" and in finance often referred to as risk.
        Reference:
            www.moneycontrol.com

        Returns:
            pd.DataFrame: Pandas DataFrame
        """
        data = self.df.copy()
        data = data.sort_values(by=self.date_col).reset_index(drop=True)
        v = np.log(data[self.price_col]).diff().rolling(volatile_period).std() * np.sqrt(365)
        df_bvol = pd.DataFrame(data={'BVOL_Index': v})
        data = pd.concat([data, df_bvol], join="inner", axis=1)
        data = data.dropna()
        data = data.sort_values(by=self.date_col, ascending=False).reset_index(
            drop=True
        )
        return data

    @staticmethod
    def get_vola_graph(
        data: pd.DataFrame, output_path: Optional[str] = "bvol_index.png"
    ) -> None:
        """
        Make a line graph of volatile index with respect to time
        Args:
            data(pd.DataFrame): Output of get_vola_index function
            output_path(str): Path to save plot
        """

        fig, ax = plt.subplots(figsize=(14, 12))
        rect = fig.patch
        rect.set_facecolor("yellow")
        ax1 = plt.subplot(211)
        ax1.plot(data["date"], data["price"], color="blue", label="Price")
        plt.ylabel("Price", color="red", fontsize=20)
        ax1.axes.get_xaxis().set_ticks([])
        plt.legend()
        ax1.tick_params(axis="y", colors="b")
        ax1.grid(color="grey", linestyle="-", linewidth=0.25, alpha=0.5)

        ax2 = plt.subplot(212)
        ax2.plot(
            data["date"], data["BVOL_Index"], color="b", label="BVOL Index"
        )
        plt.xlabel("Time", color="red", fontsize=20)
        plt.ylabel("Volatility Index", color="r", fontsize=20)
        plt.legend()
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=90)
        ax2.grid(color="grey", linestyle="-", linewidth=0.25, alpha=0.5)

        ax2.tick_params(axis="x", colors="b")
        ax2.tick_params(axis="y", colors="b")

        plt.suptitle("Price  and  Volatility Index", color="red", fontsize=24)
        plt.savefig(output_path, bbox_inches="tight", facecolor="orange")
        plt.show()

    def get_rsi(self) -> pd.DataFrame:
        """
        Type:
            Momentum indicator

        Computation:
                    It is based on the average price increase during a period of
                    rising prices and average price fall during a period of
                    falling stock prices. Relative Strength Index (RSI) is
                    plotted between 0 and 100.

        What it signals:
                        Usually, the market is treated as overbought when RSI
                        goes above 70 (80 for highly volatile stocks) and
                        oversold when it hits 30—20 for highly volatile stocks.

        Reference:
                    https://economictimes.indiatimes.com/
        Returns:
            pd.DataFrame: Pandas DataFrame with RSI values

        """
        data = self.df.copy()
        data = data.sort_values(by=self.date_col).reset_index(drop=True)
        data["price_change"] = data[self.price_col] - data[
            self.price_col
        ].shift(1)
        data.dropna(inplace=True)
        data["gain"] = np.where(data["price_change"] >= 0, data["price_change"], 0)
        data["loss"] = np.where(data["price_change"] <= 0, abs(data["price_change"]), 0)

        data["gain_average"] = data["gain"].rolling(14).mean()
        data["loss_average"] = data["loss"].rolling(14).mean()

        data["RS"] = data["gain_average"] / data["loss_average"]

        data["RSI_1"] = 100 * (1 - (1 / (1 + data["RS"])))

        data["RS_Smooth"] = (
            data["gain_average"].shift(1) * 13 + data["gain"]
        ) / (data["loss_average"].shift(1) * 13 + data["loss"])

        data["RSI_2"] = 100 * (1 - (1 / (1 + data["RS_Smooth"])))
        data = data.fillna(0).reset_index(drop=True)
        data.drop(
            [
                "gain",
                "loss",
                "price_change",
                "gain_average",
                "loss_average",
                "RS",
            ],
            axis=1,
            inplace=True,
        )
        data = data.sort_values(by=self.date_col, ascending=False).reset_index(
            drop=True
        )
        return data

    @staticmethod
    def get_rsi_graph(data: pd.DataFrame) -> None:
        """
        Plot RSI against date and price
        Args:
            data(pd.DataFrame): Output of get_rsi function.


        """
        fig, ax = plt.subplots(figsize=(14, 12))
        rect = fig.patch
        rect.set_facecolor("yellow")
        ax1 = plt.subplot(211)
        ax1.plot(data["date"], data["price"], color="blue", label="Price")
        plt.ylabel("Price ($)", color="red", fontsize=20)
        ax1.axes.get_xaxis().set_ticks([])
        plt.legend()
        ax1.tick_params(axis="y", colors="b")

        ax2 = plt.subplot(212)
        ax2.plot(data["date"], data["RSI_2"], color="b", label="RSI")
        plt.xlabel("Time", color="red", fontsize=20)
        plt.ylabel("Relative Strength Index (RSI)", color="r", fontsize=20)
        plt.text(
            data["date"][int(len(data) / 2)],
            80,
            ">70 OverBought",
            fontsize=20,
            color="black",
        )
        plt.text(
            data["date"][int(len(data) / 2)],
            15,
            "<30 OverSold",
            fontsize=20,
            color="black",
        )
        plt.legend()
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=90)

        ax2.tick_params(axis="x", colors="b")
        ax2.tick_params(axis="y", colors="b")

        ax2.axhline(y=70, color="r")
        ax2.axhline(y=30, color="r")

        plt.suptitle(
            "Price  and  Relative  Strength Index", color="red", fontsize=24
        )
        plt.savefig("rsi.png", bbox_inches="tight", facecolor="orange")
        plt.show()

    def get_bollinger_bands(
        self,
        days: Optional[int] = 20,
        plot: Optional[bool] = False,
        out_path: Optional[str] = "bollinger_bands.png",
    ) -> pd.DataFrame:
        """
        Type:
            Trend, volatility, momentum indicator

        Computation:
                    They comprise three lines: A 20-day moving average, an upper
                    band and lower band—the upper and lower bands are plotted as
                    two standard deviations from the moving average.

        What it signals:
                        The moving average shows the trend, the gap between
                        upper and lower band shows volatility in the counter.

        References:
                   1.  https://economictimes.indiatimes.com/
                   2. https://www.bollingerbands.com/bollinger-bands
        Args:
            days (int): Number of days to calculate moving average
            plot (bool): If plot bollinger bands
            out_path (str): Save path for plot

        Returns:
            pd.DataFrame: A pandas DataFrame and save a plot to given path.

        """
        data = self.df.copy()
        data = data.sort_values(by=self.date_col).reset_index(drop=True)
        data["SMA"] = data[self.price_col].rolling(days).mean()
        data["SD"] = data[self.price_col].rolling(days).std()
        data["BB_upper"] = data["SMA"] + data["SD"] * 2
        data["BB_lower"] = data["SMA"] - data["SMA"] * 2
        data.drop(["SD", "SMA"], axis=1, inplace=True)
        data = data.sort_values(by=self.date_col, ascending=False).reset_index(
            drop=True
        )
        while plot:
            fig, ax = plt.subplots(figsize=(16, 12))
            plt.plot(data[self.date_col], data["BB_upper"], color="g")
            plt.plot(data[self.date_col], data["BB_lower"], color="g")
            plt.plot(data[self.date_col], data[self.price_col], color="orange")
            plt.legend()
            plt.xlabel("Time", color="b", fontsize=22)
            plt.ylabel("Price", color="b", fontsize=22)
            plt.title("Bollinger Bands", color="b", fontsize=27)
            plt.tick_params(labelsize=17)
            fig.set_facecolor("yellow")
            plt.grid()
            plt.savefig(
                out_path, bbox_inches="tight", facecolor="orange",
            )
            plt.show()
            break
        return data

    def get_moving_average_convergence_divergence(
        self, plot: Optional[bool] = False, out_path: Optional[str] = "macd.png"
    ) -> pd.DataFrame:
        """
        Type
            Trend and momentum indicator

        Computation
            The difference between 12 and 26-day moving averages.

        What it signals
            Rising Moving Average Convergence Divergence (MACD) indicates an
            upward price trend and falling MACD indicates a downward price trend.

        Reference:
            https://economictimes.indiatimes.com/
        Args:
            plot (bool): If plot bollinger bands
            out_path (str): Save path for plot

        Returns:
            pd.DataFrame: Pandas DataFrame with MACD values

        """
        data = self.df.copy()
        data["EMA_12"] = data[self.price_col].ewm(span=12, adjust=False).mean()
        data["EMA_26"] = data[self.price_col].ewm(span=26, adjust=False).mean()
        data["MACD"] = data["EMA_12"] - data["EMA_26"]
        data.drop(["EMA_12", "EMA_26"], axis=1, inplace=True)
        data = data.dropna()

        while plot:
            fig, ax = plt.subplots(figsize=(14, 9))
            plt.plot(
                data[self.date_col],
                data[self.price_col],
                color="r",
                label="Price",
            )
            plt.plot(data[self.date_col], data["MACD"], color="b", label="MACD")
            plt.legend()
            plt.title("Price and MACD Plot", fontsize=28, color="b")
            plt.xlabel("Time", color="b", fontsize=19)
            plt.ylabel("Price", color="b", fontsize=19)
            plt.savefig(out_path, bbox_inches="tight", facecolor="orange")
            fig.set_facecolor("orange")
            plt.show()
            break
        return data

    def get_simple_moving_average(
        self,
        days: Optional[int] = 15,
        plot: Optional[bool] = False,
        out_path: Optional[str] = "sma.png",
    ):
        """
        Simple moving average of given days
        Args:
            days (int): Number of days to calculate SMA
            plot (bool): If plot bollinger bands
            out_path (str): Save path for plot

        Returns:
            pd.DataFrame: Pandas DataFrame with SMA values

        """

        data = self.df.copy()
        data = data.sort_values(by=self.date_col).reset_index(drop=True)
        data["SMA"] = data[self.price_col].rolling(days).mean()
        data = data.dropna()
        data = data.sort_values(by=self.date_col, ascending=False).reset_index(
            drop=True
        )
        while plot:
            fig, ax = plt.subplots(figsize=(14, 9))
            plt.plot(
                data[self.date_col],
                data[self.price_col],
                color="r",
                label="Price",
            )
            plt.plot(data[self.date_col], data["SMA"], color="b", label="SMA")
            plt.legend()
            plt.title("Price and SMA Plot", fontsize=28, color="b")
            plt.xlabel("Time", color="b", fontsize=19)
            plt.ylabel("Price", color="b", fontsize=19)
            plt.savefig(out_path, bbox_inches="tight", facecolor="orange")
            fig.set_facecolor("orange")
            plt.show()
            break
        return data

    def get_exponential_moving_average(
        self,
        periods: List[int] = [20],
        plot: Optional[bool] = False,
        out_path: Optional[str] = "ema.png",
    ):
        """
        The EMA is a moving average that places a greater weight and
        significance on the most recent data points. Like all moving averages,
        this technical indicator is used to produce buy and sell signals based
        on crossovers and divergences from the historical average.

        Traders often use several different EMA days, for instance, 20-day,
        30-day, 90-day, and 200-day moving averages.
        Reference:
            https://www.investopedia.com/
        Args:
            periods (list): List of period to calculate EMA
            days (int): Number of days to calculate SMA
            plot (bool): If plot bollinger bands
            out_path (str): Save path for plot

        Returns:
            pd.DataFrame: Pandas DataFrame with EMA values
        """
        data = self.df.copy()
        for period in periods:
            data["EMA_{}".format(period)] = (
                data[self.price_col].ewm(span=period, adjust=False).mean()
            )
        while plot:
            fig, ax = plt.subplots(figsize=(14, 9))
            plt.plot(
                data[self.date_col],
                data[self.price_col],
                color="r",
                label="Price",
            )
            for period in periods:
                plt.plot(
                    data[self.date_col],
                    data["EMA_{}".format(period)],
                    label="EMA_{}".format(period),
                )
            plt.legend()
            plt.title("Price and EMA Plot", fontsize=28, color="b")
            plt.xlabel("Time", color="b", fontsize=19)
            plt.ylabel("Price/EMA", color="b", fontsize=19)
            plt.savefig(out_path, bbox_inches="tight", facecolor="orange")
            fig.set_facecolor("orange")
            plt.show()
            break
        return data
