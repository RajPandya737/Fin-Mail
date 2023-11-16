from financial_data import FinancialData
from pdf import PDF

equity = ["SPY","^IXIC","^DJI", "^VIX"]
stocks = ['HBM', 'L.TO', 'APO', "MA", "AAPL", "EA", "TEX", "CEG", "ISRG"]
resources = ["GC=F", "SI=F", "PL=F", "PA=F", "HG=F"]
commodities = ["CL=F", "GC=F", "NG=F"]
treasury = ["^IRX", "^FVX", "^TNX", "^TYX"]


data = FinancialData()

pdf = PDF()
pdf.create_header("Equity")
pdf.create_table(data.get_equity_data(equity))
pdf.create_header("Treasury Yields")
pdf.create_table(data.get_equity_data(treasury))
pdf.create_header("Stocks")
pdf.create_table(data.get_equity_data(stocks))
pdf.create_header("Resources")
pdf.create_table(data.get_equity_data(resources))
pdf.create_header("Commodities")
pdf.create_table(data.get_equity_data(commodities))
pdf.create_header("Currency (USD)")
pdf.create_table(data.get_currency_data())

pdf.save()

