from fpdf import FPDF

class PDF:
    def __init__(self, file_name="output.pdf"):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        self.file_name = file_name
        self.page_width = self.pdf.w - 0.5 * self.pdf.l_margin
        self.page_height = self.pdf.h - 0.5 * self.pdf.t_margin

    def set_header(self):
        self.pdf.set_fill_color(120, 0, 0)  # Dark Red background color
        self.pdf.set_text_color(255, 255, 255)  # White text color
        x_position = (self.pdf.w - self.page_width) / 2
        y_position = (self.pdf.h - self.page_height) / 2
        self.pdf.set_xy(x_position, y_position)
        self.pdf.cell(self.page_width, 8, 'DFIC Daily Report', 0, 1, 'C', 1)

    def save_pdf(self):
        self.pdf.output(self.file_name)

# Example usage:
pdf = PDF("simple_demo.pdf")
pdf.set_header()
pdf.save_pdf()
