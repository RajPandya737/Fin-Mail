from financial_data import FinancialData
from pdf import PDF

equity = ["SPY","^IXIC","^DJI", "^VIX"]
stocks = ['HBM', 'L', 'APO', "MA", "AAPL", "EA", "TEX", "CEG", "ISRG"]
metals = ["GC=F", "SI=F", "PL=F", "PA=F", "HG=F"]

data = FinancialData()

pdf = PDF()
pdf.create_table(data.get_equity_data(equity))
pdf.create_table(data.get_equity_data(stocks))
pdf.create_table(data.get_equity_data(metals))

pdf.save()

