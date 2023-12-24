import pandas as pd

class Excel:
    def __init__(self):
        self.titles = []
        self.data = []
        self.n = 0

    def add_data(self, title, data):
        self.titles.append(title)
        self.data.append(data)
        
    def save(self):
        equity_mapping = {
            "SPY": "S&P 500 ETF",
            "^IXIC": "Nasdaq Composite",
            "^DJI": "Dow Jones Industrial Average",
            "^VIX": "CBOE Volatility Index",
            'HBM': 'Hudbay Minerals Inc.',
            'L.TO': 'Loblaw Companies Limited',
            'APO': 'Apollo Global Management, Inc.',
            'MA': 'Mastercard Incorporated',
            'AAPL': 'Apple Inc.',
            'EA': 'Electronic Arts Inc.',
            'TEX': 'Terex Corporation',
            'CEG': 'Constellation Energy Corporation',
            'ISRG': 'Intuitive Surgical, Inc.',
            'GC=F': 'Gold Futures',
            'SI=F': 'Silver Futures',
            'PL=F': 'Platinum Futures',
            'PA=F': 'Palladium Futures',
            'HG=F': 'Copper Futures',
            'CL=F': 'Crude Oil Futures',
            'NG=F': 'Natural Gas Futures',
            "AUDUSD=X": "Australian Dollar",
            "CADUSD=X": "Canadian Dollar",
            "EURUSD=X": "Euro",
            "JPYUSD=X": "Japanese Yen",
            "NZDUSD=X": "New Zealand Dollar",
            "NOKUSD=X": "Norwegian Krone",
            "GBPUSD=X": "British Pound",
            "SEKUSD=X": "Swedish Krona",
            "RUBUSD=X": "Russian Ruble",
            "CHFUSD=X": "Swiss Franc",
            "^IRX": "3 Month Treasury Yield",
            "^FVX": "5 Year Treasury Yield", 
            "^TNX": "10 Year Treasury Yield", 
            "^TYX": "30 Year Treasury Yield",
            "SHY": "iShares 1-3 Yr Treasury ETF",
            "IEI": "iShares 3-7 Yr Treasury ETF",
            "IEF": "iShares 7-10 Yr Treasury ETF",
            "STIP": "BlackRock 0-5 Yr TIPS ETF",
            "TLT": "iShares 20+ Yr Treasury ETF",
            "SHV": 'iShares Short Treasury',
            "BIL": 'SPDR 1-3 Month T-Bill',
            "SCHO": 'SPDR Short Term Treasury',
            "SCHR": 'SPDR Intermediate Term Treasury',
            "SPSB": 'SPDR Short Term Corporate Bond',
            "CDN.AVG.1YTO3Y.AVG": "1-3 Year Treasury Yield", 
            "BD.CDN.2YR.DQ.YLD": "2 Year Treasury Yield",
            "BD.CDN.5YR.DQ.YLD": "5 Year Treasury Yield",
            "BD.CDN.10YR.DQ.YLD": "10 Year Treasury Yield",
            "T5YIE": "5 Year TIPS Yield", 
            "T10YIE": "10 Year TIPS Yield", 
            "T30YIEM": "30 Year TIPS Yield"
        }
        
        days_mapping = {
            "today": "Price",
            "p_diff_yesterday": "1d",
            "p_diff_week": "1w",
            "p_diff_month": "1m",
            "p_diff_three_months": "3m",
            "p_diff_six_months": "6m",
            "p_diff_year_to_date": "Ytd",
            "p_diff_year": "1y",
            "p_diff_five_year": "5y"
        }
        # for i, d in enumerate(self.data):
        #     self.data[i] = {equity_mapping[key]: {days_mapping[sub_key]: sub_value for sub_key, sub_value in value.items()} for key, value in d.items()}
        # list_of_dfs = [pd.DataFrame(data) for data in self.data]
        # result_df = pd.concat(list_of_dfs, axis=1).transpose()
        # result_df.to_excel(f'output.xlsx', index_label='Row')
        
        for i, d in enumerate(self.data):
            self.data[i] = {equity_mapping[key]: {days_mapping[sub_key]: sub_value for sub_key, sub_value in value.items()} for key, value in d.items()}

        # Create DataFrames and concatenate
        list_of_dfs = [pd.DataFrame(d) for d in self.data]
        result_df = pd.concat(list_of_dfs, axis=1).transpose()

        with pd.ExcelWriter('Daily Excel Report.xlsx', engine='xlsxwriter') as writer:
            result_df.to_excel(writer, index_label='Row')

            # Access the XlsxWriter workbook and worksheet objects
            workbook  = writer.book
            worksheet = writer.sheets['Sheet1']

            # Set the width for the first column (Column A) to a specific value (e.g., 30)
            worksheet.set_column(0, 0, 30)