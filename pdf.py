from fpdf import FPDF



class PDF:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        page_width = self.pdf.w - 0.5 * self.pdf.l_margin
        page_height = self.pdf.h - 0.5 * self.pdf.t_margin
        # pdf.set_fill_color(120, 0, 0)
        # pdf.set_text_color(255, 255, 255)
        # x_position = (pdf.w - page_width) / 2
        # y_position = (pdf.h - page_height) / 2
        # pdf.set_xy(x_position, y_position)
        # pdf.cell(page_width, 8, 'DFIC Daily Report', 0, 1, 'C', 1)

    def create_table(self, data):
        first_inner_dict_key = list(data.keys())[0]
        first_inner_dict = data[first_inner_dict_key]
        columns = list(first_inner_dict.keys())

        column_widths = [self.pdf.get_string_width(str(col)) + 10 for col in columns]

        self.pdf.cell(column_widths[0], 5, txt='', border=1)

        for index, (width, col) in enumerate(zip(column_widths[1:], columns[1:])):
            self.pdf.cell(width, 5, txt=col, border=1)
        self.pdf.ln()

        for key, sub_dict in data.items():
            self.pdf.cell(column_widths[0], 5, txt=str(key), border=1)
            for index, (col, width) in enumerate(zip(columns[1:], column_widths[1:])):
                self.pdf.cell(width, 5, txt=str(sub_dict[col]), border=1)
            self.pdf.ln()


    def save(self):
        self.pdf.output("output.pdf")
