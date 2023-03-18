import requests
import pandas as pd
import toml
import mplfinance as mpf
import json
from indicators import calculate_atr, calculate_macd
import numpy as np

# Setting the api key in the config
config = toml.load("secrets.toml")
API_KEY = config["API"]["api_key"]

# Caching API requests
cache = {}


def get_data_from_api(
    key, func: str, from_symbol: str, to_symbol: str, outputsize: str
):
    if (key, func, from_symbol, to_symbol, outputsize) in cache:
        return cache[(key, func, from_symbol, to_symbol, outputsize)]
    else:
        url = f"https://www.alphavantage.co/query?function={func}&from_symbol={from_symbol}&to_symbol={to_symbol}&outputsize={outputsize}&apikey={key}"
        response = requests.get(url)
        try:
            data_dict = response.json()
        except json.JSONDecodeError:
            raise ValueError(f"Response is not in JSON format: {response.content}")
        cache[(key, func, from_symbol, to_symbol, outputsize)] = data_dict
        return data_dict


def save_data_to_json(data):
    with open("ohlc.json", "w") as jsonfile:
        json.dump(data, jsonfile, indent=4)


# Getting data from API and creating DataFrame
data_dict = get_data_from_api(API_KEY, "FX_DAILY", "AUD", "USD", "full")
save_data_to_json(data_dict)
df = pd.DataFrame(data_dict[list(data_dict.keys())[-1]]).transpose()
df.columns = ["Open", "High", "Low", "Close"]
df = df.astype(float)
df.index = pd.to_datetime(df.index)
df = df.iloc[::-1]
start_date = "2020-01-03"  #! YYYY-MM-DD
end_date = list(data_dict[list(data_dict.keys())[-1]].keys())[0]
"""I know that getting the end_date looks ugly but it does the job. It's gonna take the first element of the Time Series Key.
The reason for that is because Time Series Key name is based on parameters given to the get_data_from_api"""
df = df.loc[start_date:end_date]
# Creating the Heiken Ashi DataFrame
ha_close = (df["Open"] + df["High"] + df["Low"] + df["Close"]) / 4
ha_open = (df["Close"].shift(1) + df["Open"].shift(1)) / 2
ha_open.iloc[0] = df["Open"].iloc[0]
ha_high = pd.concat([df["High"], ha_open, ha_close], axis=1).max(axis=1)
ha_low = pd.concat([df["Low"], ha_open, ha_close], axis=1).min(axis=1)
heiken_ashi_df = pd.DataFrame(
    {"Open": ha_open, "High": ha_high, "Low": ha_low, "Close": ha_close}
)
heiken_ashi_df.index = pd.to_datetime(heiken_ashi_df.index)

atr_values = calculate_atr(heiken_ashi_df, 14)
atr_plot = mpf.make_addplot(atr_values, panel=2, ylabel="Average True Range")

macd_line, signal_line, histogram = calculate_macd(heiken_ashi_df, 12, 26, 9)
hist_colors = np.where(histogram >= 0, "orange", "red")
ap_macd = mpf.make_addplot(macd_line, panel=1, ylabel="MACD", color="purple")
ap_signal = mpf.make_addplot(signal_line, panel=1, ylabel="Signal Line", color="pink")
ap_histogram = mpf.make_addplot(
    histogram, type="bar", panel=1, ylabel="Histogram", color=hist_colors
)

# Plotting the candlestick chart
mpf.plot(
    heiken_ashi_df,
    type="candle",
    style="yahoo",
    mav=[10, 20, 50, 100],
    ylabel="Exchange Rate",
    title="AUD/USD exchange ratio",
    addplot=[ap_macd, ap_signal, ap_histogram, atr_plot],
)
