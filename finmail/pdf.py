from fpdf import FPDF
from config import COL_WIDTH, FONT_SIZE, IMAGE_RATIO, IMAGE_OFFSET
from PIL import Image
from math import isnan


class PDF:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.font_size = FONT_SIZE
        self.pdf.set_font("helvetica", size=self.font_size)
        self.page_width = self.pdf.w - 0.5 * self.pdf.l_margin
        self.page_height = self.pdf.h - 0.5 * self.pdf.t_margin
        self.image_x = IMAGE_OFFSET
        self.image_y = 0
        self.added_images = False

    
    def reset(self):

        self.pdf.set_font("helvetica", size=self.font_size)
        self.page_width = self.pdf.w - 0.5 * self.pdf.l_margin
        self.page_height = self.pdf.h - 0.5 * self.pdf.t_margin
        
    def create_header(self, header, align='L', back=True):
        self.pdf.set_font("helvetica", 'B', self.font_size)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.ln(1)
        if back:
            self.pdf.set_fill_color(220, 220, 220)
        else:
            self.pdf.set_fill_color(255, 255, 255)
        self.pdf.rect(10, self.pdf.get_y(), self.pdf.w-20, 4, 'F')

        self.pdf.cell(0, 2, header, ln=True, align=align)
        self.reset()
        
    def create_table(self, data, type="dollar", final=False):
        self.pdf.ln(3)

        self.pdf.set_font("helvetica", size=self.font_size)
        first_inner_dict_key = list(data.keys())[0]
        first_inner_dict = data[first_inner_dict_key]
        columns = list(first_inner_dict.keys())
        column_widths = [max([self.pdf.get_string_width(str(col)) + 10 for col in columns]) for col in columns]

        self.pdf.cell(column_widths[0]+5, 5, txt='', border=0)

        ticker_to_name = {
            "XIU.TO": "iShares S&P/TSX 60",
            "XBB.TO": "iShares Core Canadian Bond",
            "HBM": "Hudbay Minerals",
            "L.TO": "Loblaw",
            "WFG.TO": "West Fraser Timber",
            "CSH-UN.TO": "iShares S&P/TSX Capped Financials",
            "AGG": "iShares Core U.S. Aggregate",
            "SPY": "SPDR S&P 500",
            "APO": "Apollo Global Management",
            "AAPL": "Apple",
            "CEG": "Centennial Resource Development",
            "EA": "Electronic Arts",
            "ISRG": "Intuitive Surgical",
            "MA": "Mastercard",
            "TEX": "Terex",
            "AMSF": "AMERISAFE",
            "VEEV": "Veeva Systems",
            "GSL": "Global Ship Lease",
            "SPSB": "SPSB"
        }

        equity_mapping = {
            "XIU.TO": "iShares S&P/TSX 60",
            "XBB.TO": "iShares Core Canadian Bond",
            "HBM": "Hudbay Minerals",
            "L.TO": "Loblaw",
            "WFG.TO": "West Fraser Timber",
            "CSH-UN.TO": "iShares S&P/TSX Capped",
            "AGG": "iShares Core U.S. Aggregate",
            "SPY": "SPDR S&P 500",
            "APO": "Apollo Global Management",
            "AAPL": "Apple",
            "CEG": "Centennial Resource Development",
            "EA": "Electronic Arts",
            "ISRG": "Intuitive Surgical",
            "MA": "Mastercard",
            "TEX": "Terex",
            "AMSF": "AMERISAFE",
            "VEEV": "Veeva Systems",
            "GSL": "Global Ship Lease",
            "SPSB": "SPSB",
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
            "p_diff_five_year": "5y",
            "value": "Value"
        }
        if type != "dollar":
            days_mapping["today"] = "Yield"

        for index, (width, col) in enumerate(zip(column_widths, columns)):
            self.pdf.cell(COL_WIDTH*width, 4, txt=days_mapping[col], border=0, align='R')
        self.pdf.ln()
        for key, sub_dict in data.items():
            self.pdf.cell(column_widths[0]+5, 4, txt=equity_mapping[str(key)], border=0)
            for index, (col, width) in enumerate(zip(columns, column_widths)):
                self.pdf.set_text_color(0, 0, 0)
                num = sub_dict[col]
                
                
                if isnan(num) or num == 0:
                    txt = "-"
                    val = 0

                elif index == 0 and type == "dollar":
                    txt = "${:.2f}".format(num)
                elif index == 0 and type == "yield":
                    txt = "{:.2f}%".format(num)
                # elif index == 8 and type == "dollar":
                #     txt = "${:,.2f}".format(num)
                #     val = num
                else:
                    try:
                        if type == "dollar":
                            txt = "${:,.2f}".format(num)
                        else:
                            txt = "{:.2f}%".format(abs(num))
                        val = num
                    except KeyError:
                        txt = "-"
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
        if self.added_images is False:
            self.image_y = self.pdf.get_y()
            self.added_images = True
        
        if self.image_x + width*IMAGE_RATIO+2 >= self.page_width:
            self.image_x = IMAGE_OFFSET
            self.image_y += height*IMAGE_RATIO
        if self.image_y + height*IMAGE_RATIO >= self.page_height:
            self.pdf.add_page()
            self.image_x = IMAGE_OFFSET
            self.image_y = 10
        self.pdf.image(image_path, w=width*IMAGE_RATIO, h=height*IMAGE_RATIO, x=self.image_x, y=self.image_y)
        self.image_x += width*IMAGE_RATIO
        print(self.image_x, self.image_y)


    def save(self, filename):
        self.pdf.output(f"Daily PDF Report.pdf")
    
