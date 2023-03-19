import requests
import pandas as pd
import toml
import mplfinance as mpf
import json
import numpy as np

# Most important Forex pairs #EUR/USD, USD/JPY, GBP/USD, USD/CHF.
currency_pairs = ["EURUSD", "USDJPY", "GBPUSD", "USDCHF"]

# Setting the api key in the config
config = toml.load("secrets.toml")
API_KEY = config["API"]["api_key"]

# Caching API requests .
cache = {}


def heiken_ashi(df):
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
    return heiken_ashi_df


def save_data_to_json(currency_pair, data):
    with open(f"{currency_pair}.json", "w") as jsonfile:
        json.dump(data, jsonfile, indent=4)


def get_data_for_pairs(api_key, func, pairs, outputsize):
    data = {}
    for pair in pairs:
        if (api_key, func, pair, outputsize) in cache:
            heiken_ashi_df = cache[(api_key, func, pair, outputsize)]
        else:
            url = f"https://www.alphavantage.co/query?function={func}&from_symbol={pair[:3]}&to_symbol={pair[3:]}&outputsize={outputsize}&apikey={api_key}"
            response = requests.get(url).json()
            try:
                save_data_to_json(pair, data=response)
                df = pd.DataFrame(response[list(response.keys())[-1]]).transpose()
                df.columns = ["Open", "High", "Low", "Close"]
                df = df.astype(float)
                df.index = pd.to_datetime(df.index)
                df = df.iloc[::-1]
                heiken_ashi_df = heiken_ashi(df)
            except json.JSONDecodeError:
                raise ValueError(f"Response is not in JSON format: {response.content}")
            cache[(api_key, func, pair, outputsize)] = heiken_ashi_df
        data[pair] = heiken_ashi_df
    return data


data = get_data_for_pairs(API_KEY, "FX_DAILY", currency_pairs, "full")
