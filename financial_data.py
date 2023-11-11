import yfinance as yf
from datetime import datetime, timedelta

class FinancialData:
    def __init__(self):
        pass

    def get_equity_data(self, indices):
        data = {}
        for index in indices:
            prices = {}
            equity = yf.Ticker(index)
            today = datetime.today().date() - timedelta(days=2)
            yesterday = today - timedelta(days=1)
            week = today - timedelta(days=7)
            month = today - timedelta(days=30)
            six_months = today - timedelta(days=180)
            year = today - timedelta(days=365)
            days = {"today": today, "yesterday": yesterday, "week": week, "month": month, "six_months": six_months,
                    "year": year}
            if index != "^VIX":
                historical_data = equity.history(period="2y", interval="1d")
                for ind, day in days.items():
                    try:
                        closing = round(historical_data.loc[today.strftime('%Y-%m-%d')]['Close'], 2)
                        prices[ind] = round(historical_data.loc[day.strftime('%Y-%m-%d')]['Close'], 2)
                    except Exception as e:
                        prices[ind] = 'n/a'
                        prices['p_diff_' + ind] = 'n/a'
                        print(index, e)
            else:
                historical_data = equity.history(period="2y", interval="1d")
                for ind, day in days.items():
                    try:
                        closing = round(historical_data.loc[today.strftime('%Y-%m-%d')]['Close'], 2)
                        prices[ind] = round(historical_data.loc[day.strftime('%Y-%m-%d')]['Close'], 2)
                        prices['p_diff_' + ind] = round(((closing - prices[ind]) / prices[ind]) * 100, 2)
                    except:
                        prices[ind] = 'n/a'
                        prices['p_diff_' + ind] = 'n/a'
            data[index] = prices
        return self.round_floats_in_dict(data)

    def get_currency_data(self):
        g10_currencies = [
            "EURUSD=X",
            "JPYUSD=X",
            "CADUSD=X",
            "AUDUSD=X",
            "CNYUSD=X",
            "MXNUSD=X",
            "CLPUSD=X",
            "BRLUSD=X",
            "ARSUSD=X",
            "CHFUSD=X",
            "TRYUSD=X",
            "RUBUSD=X",
            "INRUSD=X",
        ]
        today = datetime.today().date()
        yesterday = today - timedelta(days=1)
        week = today - timedelta(days=7)
        month = today - timedelta(days=30)
        six_months = today - timedelta(days=182)
        year = today - timedelta(days=365)
        days = {"today": today, "yesterday": yesterday, "week": week, "month": month, "six_months": six_months,
                "year": year}
        data = {}
        for currency_pair in g10_currencies:
            prices = {}
            historical_data = yf.download(currency_pair, period="1y", interval="1d")
            for ind, day in days.items():
                try:
                    closing = historical_data['Close'].loc[str(today)]
                    prices[ind] = historical_data['Close'].loc[str(day)]
                    prices['p_diff_' + ind] = ((closing - prices[ind]) / prices[ind]) * 100
                    prices[ind] = prices[ind]
                except:
                    prices[ind] = 'n/a'
                    prices['p_diff_' + ind] = 'n/a'
            data[currency_pair] = prices
        return self.round_floats_in_dict(data)

    def round_floats_in_dict(self, input_dict):
        def round_float(value):
            if isinstance(value, float):
                return round(value, 2)
            return value

        rounded_dict = {}
        for key, value in input_dict.items():
            if isinstance(value, dict):
                rounded_dict[key] = {k: round_float(v) for k, v in value.items()}
            else:
                rounded_dict[key] = round_float(value)

        return rounded_dict



