"""Bollinger Bands."""

import os
import pandas as pd
import arrow
import matplotlib.pyplot as plt
import urllib2
from datetime import datetime
import seaborn


def symbol_to_path(symbol, base_dir=""):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""

    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        # Retrieve the webpage as a string
        dt = datetime.now()
        day= dt.day
        month = dt.month
        year = dt.year
        url = 'http://real-chart.finance.yahoo.com/table.csv?s={0}&d={1}&e={2}&f={3}&g=d&a=0&b=29&c=1993&ignore=.csv'.format(symbol, day, month,year)
        filename = '{}.csv'.format(symbol)
        # If file already exists then don't call Yahoo
        if not os.path.isfile(filename):
            response = urllib2.urlopen(url)
            csv = response.read()

            # Save the string to a file
            csvstr = str(csv).strip("b'")

            lines = csvstr.split("\\n")
            f = open("{}.csv".format(symbol), "w")
            for line in lines:
               f.write(line + "\n")
            f.close()

        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df


def plot_data(df, title="Stock prices"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()


def get_rolling_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    return pd.rolling_mean(values, window=window)


def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    # TODO: Compute and return rolling standard deviation
    return pd.rolling_std(values, window=window)


def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    # TODO: Compute upper_band and lower_band
    upper_band = rm + rstd * 2
    lower_band = rm - rstd *2
    return upper_band, lower_band


def test_run():
    # Read data
    now = arrow.now()
    dates = pd.date_range('2015-01-01', '2017-04-24')
    symbols = ['AMZN','GOOG','FB','AAPL','GDDY']
    df = get_data(symbols, dates)

    # Compute Bollinger Bands
    # 1. Compute rolling mean
    for symbol in symbols:
        rm = get_rolling_mean(df[symbol], window=20)

        # 2. Compute rolling standard deviation
        rstd = get_rolling_std(df[symbol], window=20)

        # 3. Compute upper and lower bands
        upper_band, lower_band = get_bollinger_bands(rm, rstd)

        # Plot raw SPY values, rolling mean and Bollinger Bands

        ax = df[symbol].plot(title="Bollinger Bands", label='{}'.format(symbol))
        rm.plot(label='Rolling mean', ax=ax)
        upper_band.plot(label='upper band', ax=ax)
        lower_band.plot(label='lower band', ax=ax)

        # Add axis labels and legend
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend(loc='upper left')
        plt.show()

# Linear regression learner beginnings
# def train(x ,y):
#     self.m,self.b = favorite_linreg(x,y) # scipy or numpy favorite lin regression function
# def query(x):
#     y = self.m * x + self.b
#     return y


if __name__ == "__main__":
    test_run()
