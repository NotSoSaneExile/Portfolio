# AlphaVantage Heiken Ashi Plotter
This script currently retrieves daily foreign exchange rate data for the AUD/USD currency pair from the AlphaVantage API, calculates the Heiken Ashi candlestick chart, and plots it using mplfinance library.

## Further improvements plans
The current version is just a basic script to get things started. Eventually I'd like to allow the user to choose different financial instruments, plot live data and allow for specifiying which indicators to plot.
If time allows I'd also love to try writing some scripts that would make a trading calls and allow for backtesting the strategies.

# Getting Started
Before running the script, make sure you have the following installed:

* Python 3
* pandas
* toml
* mplfinance
* requests

You can install the dependencies by running:
`pip install -r requirements.txt` in your command line

You will also need an AlphaVantage API key. You can get a free one by signing up at https://www.alphavantage.co/.

Once you have installed the dependencies and obtained an API key, create a secrets.toml file in the same directory as the script and add your API key as follows:

`[API]`
`api_key = "your_api_key_here"`

# Running the Script
To run the script, simply execute it in your Python environment of choice:

`python main.py`

The script will retrieve daily exchange rate data for the AUD/USD currency pair from the AlphaVantage API, calculate the Heiken Ashi candlestick chart, and plot it using mplfinance. The resulting plot will be displayed in a new window.

# Modifying the Script
You can modify the start date for the exchange rate data by changing the start_date variable in the script. For example, to start from January 1, 2021, set start_date to '2021-01-01'.

You can also modify the parameters for the Heiken Ashi candlestick chart, as well as add additional technical indicators, by modifying the relevant code in the script.

# Caching API Requests
The script uses a cache to avoid making unnecessary API requests. If the same request has been made before, the script will return the cached data instead of making a new API request. The cache is stored in a dictionary called cache.
