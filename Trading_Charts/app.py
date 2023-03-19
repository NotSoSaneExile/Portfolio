import dash
import toml
import json
import pandas as pd
from dash import dcc
from dash import html
import plotly.graph_objs as go
from exchange_ratio_data.data_retriever import get_data_from_api, get_data_from_json
from components.dropdown import CurrencyPairDropdown
from components.datepicker import DatePicker

# Most important Forex pairs #EUR/USD, USD/JPY, GBP/USD, USD/CHF.
currency_pairs = ["EURUSD", "USDJPY", "GBPUSD", "USDCHF"]

# Setting the api key in the config
config = toml.load("secrets.toml")
API_KEY = config["API"]["api_key"]

### data = get_data_for_pairs(API_KEY, "FX_DAILY", currency_pairs, "full") standard API call frequency is 5 calls per minute and 500 calls per day. Gotta use saved .jsons for demonstration

# Load data from json files ### function argument
eurusd_data = get_data_from_json("EURUSD")
usdjpy_data = get_data_from_json("USDJPY")
gbpusd_data = get_data_from_json("GBPUSD")
usdchf_data = get_data_from_json("USDCHF")

eurusd_df = pd.DataFrame(eurusd_data)
usdjpy_df = pd.DataFrame(eurusd_data)
gbpusd_df = pd.DataFrame(eurusd_data)
usdchf_df = pd.DataFrame(eurusd_data)


# Create candlestick chart trace for EURUSD
eurusd_candlestick = go.Candlestick(
    x=eurusd_df.index,
    open=eurusd_df["Open"],
    high=eurusd_df["High"],
    low=eurusd_df["Low"],
    close=eurusd_df["Close"],
    name="EURUSD",
)

# Create candlestick chart trace for GBPUSD
gbpusd_candlestick = go.Candlestick(
    x=gbpusd_df.index,
    open=gbpusd_df["Open"],
    high=gbpusd_df["High"],
    low=gbpusd_df["Low"],
    close=gbpusd_df["Close"],
    name="GBPUSD",
)

# Create layout with candlestick chart
layout = go.Layout(
    title="OHLC Data",
    xaxis=dict(title="Date"),
    yaxis=dict(title="Price"),
    hovermode="x",
)

# Create figure with candlestick traces and layout
fig = go.Figure(data=[eurusd_candlestick, gbpusd_candlestick], layout=layout)

# Define app layout
app = dash.Dash(__name__)
dropdown = CurrencyPairDropdown(id="currency-pair-dropdown")
datepicker = DatePicker(id="date-picker")
app.layout = html.Div(
    [
        dropdown.get_dropdown(),
        datepicker.get_date_picker(),
        dcc.Graph(id="ohlc-chart", figure=fig),
    ]
)

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
