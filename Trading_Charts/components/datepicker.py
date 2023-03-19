from dash import dcc
from dash.dependencies import Input, Output
import datetime


class DatePicker:
    def __init__(self, id):
        self.id = id
        self.start_date = (
            datetime.datetime.now() - datetime.timedelta(days=30)
        ).strftime("%Y-%m-%d")
        self.end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.date_picker = dcc.DatePickerRange(
            id=self.id,
            min_date_allowed=datetime.datetime(2020, 1, 1),
            max_date_allowed=datetime.datetime.now(),
            initial_visible_month=datetime.datetime.now(),
            start_date=self.start_date,
            end_date=self.end_date,
        )

    def get_date_picker(self):
        return self.date_picker

    def get_selected_dates(self, app):
        @app.callback(
            Output(self.id, "start_date"),
            Output(self.id, "end_date"),
            [Input(self.id, "start_date"), Input(self.id, "end_date")],
        )
        def update_selected_dates(start_date, end_date):
            self.start_date = start_date
            self.end_date = end_date
            return start_date, end_date

        return self.start_date, self.end_date
