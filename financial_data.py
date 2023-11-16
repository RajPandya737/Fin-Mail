import yfinance as yf
from datetime import datetime, timedelta
from config import AMT_USD

class FinancialData:
    def __init__(self):
        pass

    def get_equity_data(self, indices):
        data = {}
        for index in indices:
            prices = {}
            equity = yf.Ticker(index)
            today = datetime.today().date() - timedelta(days=1)
            yesterday = today - timedelta(days=1)
            week = today - timedelta(days=7)
            month = today - timedelta(days=30)
            six_months = today - timedelta(days=180)
            year = today - timedelta(days=365)
            days = {"today": today, "yesterday": yesterday, "week": week, "month": month, "six_months": six_months,
                    "year": year}
            historical_data = equity.history(period="2y", interval="1d")
            for ind, day in days.items():
                errors = 0
                while day <= today and errors < 5:
                    try:
                        if day == today:
                            prices[ind] = round(historical_data.loc[today.strftime('%Y-%m-%d')]['Close'], 2)
                        else:
                            closing = round(historical_data.loc[today.strftime('%Y-%m-%d')]['Close'], 2)
                            day_price = round(historical_data.loc[day.strftime('%Y-%m-%d')]['Close'], 2)
                            prices['p_diff_' + ind] = round(((closing - day_price) / day_price) * 100, 2)
                        break
                    except Exception as e:
                        day-=timedelta(days=1)
                        errors+=1
            data[index] = prices
        return self.round_floats_in_dict(data, 0)

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
        today = datetime.today().date() - timedelta(days=1)
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
            historical_data = yf.download(currency_pair, period="2y", interval="1d")
            for ind, day in days.items():
                errors = 0
                while day <= today and errors < 5:
                    try:
                        if day == today:
                            prices[ind] = AMT_USD * historical_data['Close'].loc[str(today)]
                        else:
                            closing = AMT_USD * historical_data['Close'].loc[str(today)]
                            day_price = AMT_USD * historical_data['Close'].loc[str(day)]
                            prices['p_diff_' + ind] = ((closing - day_price) / day_price) 
                        break
                    except:
                        day-=timedelta(days=1)
                        errors+=1
            data[currency_pair] = prices
        print(data)
        return self.round_floats_in_dict(data, 2)

    def round_floats_in_dict(self, input_dict, num_decimals=2):
        def round_float(value):
            if isinstance(value, float):
                return round(value, num_decimals)
            return value

        rounded_dict = {}
        for key, value in input_dict.items():
            if isinstance(value, dict):
                rounded_dict[key] = {k: round_float(v) for k, v in value.items()}
            else:
                rounded_dict[key] = round_float(value)

        return rounded_dict



