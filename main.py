import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def get_equity_data(indices):
    data = {}
    for index in indices:
        prices = {}
        equity = yf.Ticker(index)
        today = datetime.today().date()
        yesturday = today - timedelta(days=1)
        week = today - timedelta(days=7)
        month = today - timedelta(days=30)
        six_months = today - timedelta(days=180)
        year = today - timedelta(days=365)
        days = {"today": today, "yesturday": yesturday, "week": week, "month": month, "six_months": six_months, "year": year}
        if index != "^VIX":
            historical_data = equity.history(period="1y", interval="1d")
            for ind, day in days.items():
                try:
                    #print(historical_data['Close'].loc[str(day) + ' 00:00:00-04:00'])
                    closing = round(historical_data['Close'].loc[str(today) + ' 00:00:00-04:00'], 2)
                    prices[ind] = round(historical_data['Close'].loc[str(day) + ' 00:00:00-04:00'], 2)
                    prices['p_diff_' + ind] = round(((closing - prices[ind]) / prices[ind]) * 100, 2)
                except:
                    prices[ind] = 'n/a'
                    prices['p_diff_' + ind] = 'n/a'
        else:      
            historical_data = equity.history(period="1y", interval="1d")
            for ind, day in days.items():
                try:
                    closing = round(historical_data['Close'].loc[str(today) + ' 00:00:00-05:00'], 2)                  
                    prices[ind] = round(historical_data['Close'].loc[str(day) + ' 00:00:00-05:00'], 2)
                    prices['p_diff_' + ind] = round(((closing - prices[ind]) / prices[ind]) * 100, 2)
                except:
                    prices[ind] = 'n/a'
                    prices['p_diff_' + ind] = 'n/a'
        data[index] = prices
    return data

def get_currency_data():
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
    yesturday = today - timedelta(days=1)
    week = today - timedelta(days=7)
    month = today - timedelta(days=30)
    six_months = today - timedelta(days=182)
    year = today - timedelta(days=365)
    days = {"today": today, "yesturday": yesturday, "week": week, "month": month, "six_months": six_months, "year": year}
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
    return data

equity = ["SPY","^IXIC","^DJI", "^VIX"]
#equity_data = get_equity_data(equity)
#print(equity_data)


def download_stock_data(stocks):
    data = {}
    for stock in stocks:
        try:
            stock_data = yf.download(stock, period="1d", interval="1d")['Adj Close']
            data[stock] = stock_data
        except:
            print(f"Failed to download data for {stock}")
    return data

def download_currency_data(currencies, start_date, end_date):
    data = {}
    for currency in currencies:
        try:
            symbol = f"{currency}=X"  # Append '=X' to the currency symbol for Yahoo Finance
            currency_data = yf.download(symbol, start=start_date, end=end_date)
            data[currency] = currency_data
            print(f"Downloaded data for {currency}")
        except:
            print(f"Failed to download data for {currency}")
    return data


stocks = ['HBM', 'L', 'APO', "MA", "AAPL", "EA", "TEX", "CEG", "ISRG"]
metals = ["GC=F", "SI=F", "PL=F", "PA=F", "HG=F", "NYMEX/HS"]
print(get_equity_data(metals))
#download_stock_data(stocks)
#still need usdollar value


