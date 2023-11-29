from fpdf import FPDF
from config import COL_WIDTH, FONT_SIZE, IMAGE_RATIO
from PIL import Image


class PDF:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.font_size = FONT_SIZE
        self.pdf.set_font("Arial", size=self.font_size)
        self.page_width = self.pdf.w - 0.5 * self.pdf.l_margin
        self.page_height = self.pdf.h - 0.5 * self.pdf.t_margin

    
    def reset(self):

        self.pdf.set_font("Arial", size=self.font_size)
        self.page_width = self.pdf.w - 0.5 * self.pdf.l_margin
        self.page_height = self.pdf.h - 0.5 * self.pdf.t_margin
        
    def create_header(self, header):
        self.pdf.set_font("Arial", 'B', self.font_size)
        self.pdf.set_fill_color(220, 220, 220)  
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
            "p_diff_year": "1y",
            "p_diff_five_year": "5y"
        }

        for index, (width, col) in enumerate(zip(column_widths, columns)):
            self.pdf.cell(COL_WIDTH*width, 4, txt=days_mapping[col], border=0, align='R')
        self.pdf.ln()
        print(data)
        for key, sub_dict in data.items():
            self.pdf.cell(column_widths[0]+5, 4, txt=equity_mapping[str(key)], border=0)
            for index, (col, width) in enumerate(zip(columns, column_widths)):
                self.pdf.set_text_color(0, 0, 0)
                if index == 0:
                    txt = "${:.2f}".format(sub_dict[col])
                else:
                    try:
                        txt = "{:.2f}%".format(abs(sub_dict[col]))
                        val = sub_dict[col]
                    except KeyError:
                        txt = "n/a"
                        val = 0
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
    
    def add_image(self, image_path, x, y):
        image_path = image_path
        image = Image.open(image_path)

        # Get the dimensions (width x height) of the image
        width, height = image.size
        self.pdf.image(image_path, w=width*IMAGE_RATIO, h=height*IMAGE_RATIO)


    def save(self, filename):
        self.pdf.output(f"{filename}.pdf")
    
