from financial_data import FinancialData
from pdf import PDF
import schedule
import time
from excel import Excel
from Plot import Plot
from config import DARK_RED, OFFSET
import os
import dotenv
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import json


dotenv.load_dotenv()

def retireve_pdf():
    cad_port = ["XIU.TO", "XBB.TO", "HBM", "L.TO", "WFG.TO", "CSH-UN.TO"]
    us_port = ["AGG", "SPY", "APO", "AAPL", "CEG", "EA", "ISRG", "MA", "TEX", "AMSF", "VEEV", "GSL", "SPSB"]
    #equity = ["SPY","^IXIC","^DJI", "^VIX"]
    #stocks = ['HBM', 'L.TO', 'APO', "MA", "AAPL", "EA", "TEX", "ISRG", "CEG"]
    resources = ["GC=F", "SI=F", "PL=F", "PA=F", "HG=F"]
    us_treasury = ["^IRX", "^FVX", "^TNX", "^TYX"]
    commodities = ["CL=F", "GC=F", "NG=F"]



    data = FinancialData()


    pdf = PDF()
    excel = Excel()
    cad_data = data.get_equity_data(cad_port)
    print(cad_data)

    
    
    us_data = data.get_equity_data(us_port)
    #stocks_data["CEG"]['p_diff_five_year'] = 0

    days = 4

    with open(os.path.join(os.getcwd(), 'dfic_holdings.json'), 'r') as file:
        data_dict = json.load(file)

    for key in cad_data:
        cad_data[key]['value'] = round(data_dict[key] * data.get_port_price(key), 2)

    for key in us_data:
        us_data[key]['value'] = round(data_dict[key] * data.get_port_price(key), 2)


    total_portfolio = data.calculate_portfolio()

    pdf.create_header("Total Portfolio Value: $" + (f"{total_portfolio:,.2f}" if total_portfolio >= 100000 else f"{total_portfolio:.2f}"))

    pdf.create_header("CAD Portfolio")
    pdf.create_table(cad_data)
    excel.add_data("Equity", cad_data)

    pdf.create_header("US Portfolio")
    pdf.create_table(us_data)
    excel.add_data("Stocks", us_data)
    
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
    tips = data.get_us_tips_data()
    us_treasury_data.update(tips)
    
    
    pdf.create_header("US Treasury Yields")
    pdf.create_table(us_treasury_data, type="yield")
    excel.add_data("US Treasury Yields", us_treasury_data)
    
    
        
    cad_treasury_data = data.get_cad_bond_data()
    pdf.create_header("CAD Treasury Yields")
    pdf.create_table(cad_treasury_data, type="yield")
    excel.add_data("CAD Treasury Yields", cad_treasury_data)
    
    
    # P = Plot()
    # add_plot(P, "SPY", "S&P 500 ETF", data, pdf)
    # add_plot(P, "HBM", "Hudbay Minerals", data, pdf)
    # add_plot(P, "AAPL", "Apple", data, pdf)
    # add_plot(P, "GC=F", "Gold Futures", data, pdf)


    # # P.plot(data.daily_data["SPY"], num_years=5, title="S&P 500 ETF", xlabel="Date", ylabel="Price", color1=DARK_RED, linewidth=3.0, label="SPY Price", name='SPY')
    # # P.reset_plot()
    # # pdf.add_image("SPY.png", 0,0)
    
    
    # # P.plot(data.daily_data["HBM"], num_years=5, title="HBM Price", xlabel="Date", ylabel="Price", color1=DARK_RED, linewidth=3.0, label="HBM Price", name='HBM')
    # # pdf.add_image("HBM.png", 0,0)
    # # P.reset_plot()
    # # P.plot(data.daily_data["AAPL"], num_years=5, title="AAPL Price", xlabel="Date", ylabel="Price", color1=DARK_RED, linewidth=3.0, label="AAPL Price", name='AAPL')

    # # pdf.add_image("AAPL.png", 0,0)

    #excel.save()
    pdf.save('output')

    print(data.calculate_portfolio())

def add_plot(P, ticker, name, data, pdf):
    P.plot(data.daily_data[ticker], num_years=5, title=f"{name}", xlabel="Date", ylabel="Price", color1=DARK_RED, linewidth=3.0, label=f"{ticker} Price", name=name)
    P.reset_plot()
    pdf.add_image(os.path.join('graphs', f"{name}.png"), 0, 0)    

def email_pdf():
    email_sender = "finmaildailyreport@gmail.com"
    email_password = os.getenv('EMAIL_PASSWORD')
    email_reciever = "finmaildailyreport@gmail.com"
    date = datetime.now().strftime("%m/%d/%Y")
    subject = f"Daily Financial Report for {date}"
    
    message = MIMEMultipart()
    message["From"] = email_sender
    message["To"] = email_reciever
    message["Subject"] = subject
    
    body = ""
    message.attach(MIMEText(body, "plain"))
    
    pdf_attachment_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Daily PDF Report.pdf")
    with open(pdf_attachment_path, "rb") as pdf_file:
        pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
        pdf_attachment.add_header("Content-Disposition", f"attachment; filename=Daily PDF Report")
        message.attach(pdf_attachment)
        
    excel_attachment_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Daily Excel Report.xlsx")
    with open(excel_attachment_path, "rb") as excel_file:
        excel_attachment = MIMEApplication(excel_file.read(), _subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        excel_attachment.add_header("Content-Disposition", f"attachment; filename={os.path.basename(excel_attachment_path)}")
        message.attach(excel_attachment)
    smtp_server = "smtp.gmail.com" 
    smtp_port = 587  
    smtp_username = email_sender
    smtp_password = email_password
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Use TLS for security
        server.login(smtp_username, smtp_password)
        
        server.sendmail(email_sender, email_reciever, message.as_string())
    print("email sent")

    
def run():
        retireve_pdf()
        email_pdf()
    # try:
    #     pass
    # except Exception as e:
    #     print(e)

def main(): 

    schedule.every(20).seconds.do(run) 

    while True:
        schedule.run_pending()
        time.sleep(1)

#main()
run()