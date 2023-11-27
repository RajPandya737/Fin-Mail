from financial_data import FinancialData
from pdf import PDF
import schedule
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from excel import Excel

def retireve_pdf():
    equity = ["SPY","^IXIC","^DJI", "^VIX"]
    stocks = ['HBM', 'L.TO', 'APO', "MA", "AAPL", "EA", "TEX", "CEG", "ISRG"]
    resources = ["GC=F", "SI=F", "PL=F", "PA=F", "HG=F"]
    commodities = ["CL=F", "GC=F", "NG=F"]
    treasury = ["^IRX", "^FVX", "^TNX", "^TYX"]


    data = FinancialData()

    pdf = PDF()
    excel = Excel()
    equity_data = data.get_equity_data(equity)
    pdf.create_header("Equity")
    pdf.create_table(equity_data)
    excel.add_data("Equity", equity_data)
    
    treasury_data = data.get_equity_data(treasury)
    pdf.create_header("US Treasury Yields")
    pdf.create_table(treasury_data)
    excel.add_data("US Treasury Yields", treasury_data)
    
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
    
    # pdf.add_image("fig.png", 0,0)

    excel.save()

    pdf.save('output')
    

    
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