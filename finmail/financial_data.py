import yfinance as yf
from datetime import datetime, timedelta
from config import AMT_USD, OFFSET, YEARS
import pandas_datareader as pdr
import os
from collections import defaultdict
from fredapi import Fred
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class FinancialData:
    def __init__(self):
        print(OFFSET)
        pass
        self.daily_data = defaultdict(list)
        api_key = os.getenv('API_KEY')
        self.fred = Fred(api_key=api_key)

    def get_equity_data(self, indices):
        data = {}
        for index in indices:
            today = datetime.today().date() - timedelta(days=OFFSET)
            yesterday = today - timedelta(days=1)
            week = today - timedelta(days=7)
            month = today - timedelta(days=30)
            three_months = today - timedelta(days=90)
            six_months = today - timedelta(days=180)
            ytd = datetime(today.year, 1, 1).date()
            year = today - timedelta(days=365)
            five_year = today - timedelta(days=1825)
            print(index)
            prices = {}
            equity = yf.Ticker(index)
            days = {"today": today, "yesterday": yesterday, "week": week, "month": month, "three_months": three_months,
                "six_months": six_months, "year_to_date": ytd, "year": year, "five_year": five_year}
            historical_data = equity.history(period=f"{YEARS}y", interval="1d")
            self.daily_data[index] = historical_data['Close'].to_list()
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
        return self.round_floats_in_dict(data, 2)
    
    def get_cad_bond_data(self):
        url = "https://www.bankofcanada.ca/valet/observations/group/bond_yields_all/json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            script_directory = os.path.dirname(os.path.abspath(__file__))
            local_file_path = os.path.join(script_directory, "data.json")
            with open(local_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=2)

            def get_yield(data, date, category):
                for observation in data.get("observations", []):
                    if observation.get("d") == date:
                        return observation.get(category, {}).get("v")
                return None  
            bonds = ["CDN.AVG.1YTO3Y.AVG", "BD.CDN.2YR.DQ.YLD", "BD.CDN.5YR.DQ.YLD", "BD.CDN.10YR.DQ.YLD"]
            bond_data = {}
            for bond in bonds:
                time_hash = {"today": 0, "yesterday": 1, "week": 7, "month": 30, "three_months": 90, "six_months": 180, "year_to_date": (datetime.now() - datetime(datetime.now().year, 1, 1)).days, "year": 365, "five_year": 365 * 5}
                time_data = {}
                for period, days in time_hash.items():
                    target_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
                    while True:
                        yield_value = get_yield(data, target_date, category=bond)
                        if yield_value is not None:
                            break  
                        else:
                            target_date = (datetime.strptime(target_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
                    if period == "today":
                        time_data[period] = float(yield_value)
                    else:
                        time_data['p_diff_' + period] = round(((float(yield_value) - time_data["today"]) / time_data["today"]) * 100, 2)
                bond_data[bond] = time_data
            return self.round_floats_in_dict(bond_data, 2)
        return 0
    
    def get_us_tips_data(self):
        lengths = ["T5YIE", "T10YIE", "T30YIEM"]
        data = {}
        for length in lengths:
            history = self.fred.get_series(length)
            time_hash = {"today": 0, "yesterday": 1, "week": 7, "month": 30, "three_months": 90, "six_months": 180, "year_to_date": (datetime.now() - datetime(datetime.now().year, 1, 1)).days, "year": 365, "five_year": 365 * 5}
            time_data = {}
            for period, days in time_hash.items():
                target_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
                while True:
                    try:
                        yield_value = history[target_date]
                        break
                    except:
                        target_date = (datetime.strptime(target_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
                if period == "today":
                    time_data[period] = float(yield_value)
                else:
                    time_data['p_diff_' + period] = round(((float(yield_value) - time_data["today"]) / time_data["today"]) * 100, 2)
            data[length] = time_data
        return data
        
    def get_currency_data(self):
        g10_currencies = [
            "AUDUSD=X",
            "CADUSD=X",
            "EURUSD=X",
            "JPYUSD=X",
            "NZDUSD=X",
            "NOKUSD=X",
            "GBPUSD=X",
            "SEKUSD=X",
            "CHFUSD=X",
        ]
        other = [
            "USDCNY=X",
            "USDMXN=X",
            "USDCLP=X",
            "USDBRL=X",
            "USDARS=X",
            "USDINR=X",
            "RUBUSD=X",

        ]
        today = datetime.today().date() - timedelta(days=OFFSET)
        yesterday = today - timedelta(days=1)
        week = today - timedelta(days=7)
        month = today - timedelta(days=30)
        three_months = today - timedelta(days=90)
        six_months = today - timedelta(days=182)
        year = today - timedelta(days=365)
        five_year = today - timedelta(days=1825)
        ytd = datetime(today.year, 1, 1).date()
        days = {"today": today, "yesterday": yesterday, "week": week, "month": month, "three_months": three_months,
                "six_months": six_months, "year_to_date": ytd, "year": year, "five_year": five_year}
        data = {}
        for currency_pair in g10_currencies:
            prices = {}
            historical_data = yf.download(currency_pair, period=f"{YEARS}y", interval="1d")
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
                if errors >= 5:
                    prices['p_diff_' + ind] = 0
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



