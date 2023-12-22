from financial_data import FinancialData
from pdf import PDF
import schedule
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from excel import Excel
from plot import Plot
from config import DARK_RED
import os

def retireve_pdf():
    equity = ["SPY","^IXIC","^DJI", "^VIX"]
    stocks = ['HBM', 'L.TO', 'APO', "MA", "AAPL", "EA", "TEX", "CEG", "ISRG"]
    resources = ["GC=F", "SI=F", "PL=F", "PA=F", "HG=F"]
    us_treasury = ["^IRX", "^FVX", "^TNX", "^TYX"]
    #"SHY", "STIP", "IEI", "IEF", "TLT", "SHV", "BIL", "SCHO", "SCHR", "SPSB", "INF-1YR", "INF-10YR"
    commodities = ["CL=F", "GC=F", "NG=F"]



    data = FinancialData()

    pdf = PDF()
    excel = Excel()
    equity_data = data.get_equity_data(equity)
    print(equity_data)
    pdf.create_header("Equity")
    pdf.create_table(equity_data)
    excel.add_data("Equity", equity_data)
    
    
    stocks_data = data.get_equity_data(stocks)
    pdf.create_header("Stocks")
    pdf.create_table(stocks_data)
    excel.add_data("Stocks", stocks_data)
    
    resources_data = data.get_equity_data(resources)
    pdf.create_header("Resources")
    pdf.create_table(resources_data)
    excel.add_data("Resources", resources_data)
    
    commodities_data = data.get_equity_data(commodities)
    pdf.create_header("Commodities")
    pdf.create_table(commodities_data)
    excel.add_data("Commodities", commodities_data)
    
    currency_data = data.get_currency_data()
    pdf.create_header("Currency (USD)")
    pdf.create_table(currency_data)
    excel.add_data("Currency (USD)", currency_data)
    
    us_treasury_data = data.get_equity_data(us_treasury)
    pdf.create_header("US Treasury Yields")
    pdf.create_table(us_treasury_data)
    excel.add_data("US Treasury Yields", us_treasury_data)
    
    cad_treasury_data = data.get_cad_bond_data()
    pdf.create_header("CAD Treasury Yields")
    pdf.create_table(cad_treasury_data)
    excel.add_data("CAD Treasury Yields", cad_treasury_data)
    
    tips = data.get_us_tips_data()
    pdf.create_header("TIPS")
    pdf.create_table(tips)
    excel.add_data("US TIPS Yields", tips)
    
    
    # P = Plot()
    # add_plot(P, "SPY", "S&P 500 ETF", data, pdf)
    # add_plot(P, "HBM", "Hudbay Minerals", data, pdf)
    # add_plot(P, "AAPL", "Apple", data, pdf)
    # add_plot(P, "GC=F", "Gold Futures", data, pdf)


    # P.plot(data.daily_data["SPY"], num_years=5, title="S&P 500 ETF", xlabel="Date", ylabel="Price", color1=DARK_RED, linewidth=3.0, label="SPY Price", name='SPY')
    # P.reset_plot()
    # pdf.add_image("SPY.png", 0,0)
    
    
    # P.plot(data.daily_data["HBM"], num_years=5, title="HBM Price", xlabel="Date", ylabel="Price", color1=DARK_RED, linewidth=3.0, label="HBM Price", name='HBM')
    # pdf.add_image("HBM.png", 0,0)
    # P.reset_plot()
    # P.plot(data.daily_data["AAPL"], num_years=5, title="AAPL Price", xlabel="Date", ylabel="Price", color1=DARK_RED, linewidth=3.0, label="AAPL Price", name='AAPL')

    # pdf.add_image("AAPL.png", 0,0)



    excel.save()
    pdf.save('output')

def add_plot(P, ticker, name, data, pdf):
    P.plot(data.daily_data[ticker], num_years=5, title=f"{name}", xlabel="Date", ylabel="Price", color1=DARK_RED, linewidth=3.0, label=f"{ticker} Price", name=name)
    P.reset_plot()
    pdf.add_image(os.path.join('graphs', f"{name}.png"), 0, 0)    
# not tested yet
def email_pdf(to_email, pdf_file_path):
    retireve_pdf()
    # Set your email credentials
    sender_email = "your_email@gmail.com"
    sender_password = "your_email_password"

    # Create the MIME object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = "Daily Market Report"

    # Attach the PDF file
    with open(pdf_file_path, "rb") as file:
        attachment = MIMEApplication(file.read(), _subtype="pdf")
        attachment.add_header('Content-Disposition', f'attachment; filename="{pdf_file_path}"')
        msg.attach('output.pdf')

    # Connect to the SMTP server (in this example, using Gmail)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send the email
        server.sendmail(sender_email, to_email, msg.as_string())

    print(f"Email sent successfully to {to_email}!")

def run():
    schedule.every(10).seconds.do(retireve_pdf)

    while True:
        schedule.run_pending()
        time.sleep(1)


def test():
    retireve_pdf()

test()