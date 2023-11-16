from fpdf import FPDF
from config import COL_WIDTH


class PDF:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.font_size = 8
        self.pdf.set_font("Arial", size=self.font_size)
        self.page_width = self.pdf.w - 0.5 * self.pdf.l_margin
        self.page_height = self.pdf.h - 0.5 * self.pdf.t_margin

    
    def reset(self):

        self.pdf.set_font("Arial", size=7)
        self.page_width = self.pdf.w - 0.5 * self.pdf.l_margin
        self.page_height = self.pdf.h - 0.5 * self.pdf.t_margin
        
    def create_header(self, header):
        self.pdf.set_font("Arial", 'B', self.font_size)
        self.pdf.set_fill_color(200, 200, 200)  
        self.pdf.rect(10, self.pdf.get_y(), self.pdf.w-20, 4, 'F')  
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.ln(1)
        self.pdf.cell(0, 2, header, ln=True, align='L')
        self.reset()
        
    def create_table(self, data):
        self.pdf.ln(3)

        self.pdf.set_font("Arial", size=self.font_size)
        first_inner_dict_key = list(data.keys())[0]
        first_inner_dict = data[first_inner_dict_key]
        columns = list(first_inner_dict.keys())
        column_widths = [max([self.pdf.get_string_width(str(col)) + 10 for col in columns]) for col in columns]

        self.pdf.cell(column_widths[0]+5, 5, txt='', border=0)
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
            'USDEUR=X': 'Euro (EUR)',
            'USDJPY=X': 'Japanese Yen (JPY)',
            'USDCAD=X': 'Canadian Dollar (CAD)',
            'USDAUD=X': 'Australian Dollar (AUD)',
            'USDCNY=X': 'Chinese Yuan (CNY)',
            'USDMXN=X': 'Mexican Peso (MXN)',
            'USDCLP=X': 'Chilean Peso (CLP)',
            'USDBRL=X': 'Brazilian Real (BRL)',
            'USDARS=X': 'Argentine Peso (ARS)',
            'USDCHF=X': 'Swiss Franc (CHF)',
            'USDTRY=X': 'Turkish Lira (TRY)',
            'USDRUB=X': 'Russian Ruble (RUB)',
            'USDINR=X': 'Indian Rupee (INR)',
            "^IRX": "13 Week",
            "^FVX": "5 Year", 
            "^TNX": "10 Year", 
            "^TYX": "30 Year"
        }
        days_mapping = {
            "today": "Price",
            "p_diff_yesterday": "1d",
            "p_diff_week": "1w",
            "p_diff_month": "1m",
            "p_diff_three_months": "3m",
            "p_diff_six_months": "6m",
            "p_diff_year_to_date": "Ytd",
            "p_diff_year": "1y"
        }

        for index, (width, col) in enumerate(zip(column_widths, columns)):
            self.pdf.cell(COL_WIDTH*width, 4, txt=days_mapping[col], border=0, align='R')
        self.pdf.ln()

        for key, sub_dict in data.items():
            self.pdf.cell(column_widths[0]+5, 4, txt=equity_mapping[str(key)], border=0)
            for index, (col, width) in enumerate(zip(columns, column_widths)):
                self.pdf.set_text_color(0, 0, 0)
                if index == 0:
                    txt = "${:.2f}".format(sub_dict[col])
                else:
                    txt = "{:.2f}%".format(abs(sub_dict[col]))
                    val = sub_dict[col]
                    if val < 0:
                        self.pdf.set_text_color(188, 31, 37)
                    elif val > 0:
                        self.pdf.set_text_color(27, 140, 86)
                self.pdf.cell(COL_WIDTH* width, 4, txt=txt, border=0, align='R')
                self.pdf.set_text_color(0, 0, 0)
            self.pdf.ln(4)
        self.pdf.ln(3)
        self.reset()
        
    def int_check(self, number):
        if isinstance(number, (int, float)):
            if number.is_integer():
                return int(number)
        return number


    def save(self):
        self.pdf.output("output.pdf")
    
