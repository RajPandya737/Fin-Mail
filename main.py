from financial_data import FinancialData
from pdf import PDF

equity = ["SPY","^IXIC","^DJI", "^VIX"]
stocks = ['HBM', 'L', 'APO', "MA", "AAPL", "EA", "TEX", "CEG", "ISRG"]
resources = ["GC=F", "SI=F", "PL=F", "PA=F", "HG=F"]
commodities = ["CL=F", "GC=F", "NG=F"]
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

data = FinancialData()

pdf = PDF()
pdf.create_header("Equity")
equity_data = data.get_equity_data(equity)
pdf.create_table(equity_data)
pdf.create_header("Stocks")
pdf.create_table(data.get_equity_data(stocks))
pdf.create_header("Resources")
pdf.create_table(data.get_equity_data(resources))
pdf.create_header("Commodities")
e = data.get_equity_data(commodities)
print(e)
pdf.create_table(e)

pdf.create_header("Currency")

pdf.create_table(data.get_currency_data())

pdf.save()

