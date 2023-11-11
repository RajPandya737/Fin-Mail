from fpdf import FPDF



class PDF:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        self.page_width = self.pdf.w - 0.5 * self.pdf.l_margin
        self.page_height = self.pdf.h - 0.5 * self.pdf.t_margin
        # pdf.set_fill_color(120, 0, 0)
        # pdf.set_text_color(255, 255, 255)
        # x_position = (pdf.w - page_width) / 2
        # y_position = (pdf.h - page_height) / 2
        # pdf.set_xy(x_position, y_position)
        # pdf.cell(page_width, 8, 'DFIC Daily Report', 0, 1, 'C', 1)
    
    def reset(self):

        self.pdf.set_font("Arial", size=12)
        self.page_width = self.pdf.w - 0.5 * self.pdf.l_margin
        self.page_height = self.pdf.h - 0.5 * self.pdf.t_margin
        
    def create_header(self, header):
        self.pdf.set_font("Arial", 'B', 16)
        self.pdf.cell(0, 10, header, ln=True, align='C')
        self.pdf.ln(10)
        self.reset()
        
    def create_table(self, data):
        first_inner_dict_key = list(data.keys())[0]
        first_inner_dict = data[first_inner_dict_key]
        columns = list(first_inner_dict.keys())

        column_widths = [self.pdf.get_string_width(str(col)) + 10 for col in columns]

        self.pdf.cell(column_widths[0], 5, txt='', border=1)

        for index, (width, col) in enumerate(zip(column_widths, columns)):
            self.pdf.cell(width, 5, txt=col, border=1, align='C')
        self.pdf.ln()

        for key, sub_dict in data.items():
            self.pdf.cell(column_widths[0], 5, txt=str(key), border=1)
            for index, (col, width) in enumerate(zip(columns, column_widths)):
                self.pdf.cell(width, 4, txt=str(sub_dict[col]), border=1, align='C')
            self.pdf.ln()


    def save(self):
        self.pdf.output("output.pdf")
