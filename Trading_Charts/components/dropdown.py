from dash import dcc


class CurrencyPairDropdown:
    def __init__(self, id):
        self.id = id
        self.options = [
            {"label": "EUR/USD", "value": "EURUSD"},
            {"label": "USD/JPY", "value": "USDJPY"},
            {"label": "GBP/USD", "value": "GBPUSD"},
            {"label": "USD/CHF", "value": "USDCHF"},
        ]
        self.value = self.options[0]["value"]
        self.dropdown = dcc.Dropdown(
            id=self.id,
            options=self.options,
            value=self.value,
        )

    def get_dropdown(self):
        return self.dropdown
