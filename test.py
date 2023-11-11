from fpdf import FPDF

def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Get column headers from the first sub-dictionary
    columns = list(data[next(iter(data))].keys())

    # Set column widths based on the length of the longest data in each column
    column_widths = [pdf.get_string_width(str(col)) + 6 for col in columns]

    # Add table header
    for width, col in zip(column_widths, columns):
        pdf.cell(width, 10, txt=col, border=1)
    pdf.ln()

    # Add table rows
    for sub_dict in data.values():
        for col, width in zip(columns, column_widths):
            pdf.cell(width, 10, txt=str(sub_dict[col]), border=1)
        pdf.ln()

    pdf.output("output.pdf")

# Example data (replace this with your dictionary of dicts)
data_dict = {
    'Person 1': {'Name': 'John Doe', 'Age': 30, 'Occupation': 'Engineer'},
    'Person 2': {'Name': 'Jane Smith', 'Age': 25, 'Occupation': 'Doctor'},
    # Add more data as needed
}

create_pdf(data_dict)
