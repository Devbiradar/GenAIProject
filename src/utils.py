from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'CareerPathGPT - Roadmap', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(text):
    """
    Generates a PDF file from the given text.
    Handles encoding issues by replacing unsupported characters.
    Returns the binary content of the PDF.
    """
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Split text into lines to handle basic formatting
    lines = text.split('\n')
    for line in lines:
        # robust encoding handling
        clean_line = line.encode('latin-1', 'replace').decode('latin-1')
        
        # Handle bolding (simple heuristic for **text**)
        if "**" in line:
            pdf.set_font("Arial", 'B', 12)
            clean_line = clean_line.replace("**", "")
            pdf.multi_cell(0, 10, clean_line)
            pdf.set_font("Arial", size=12)
        else:
            pdf.multi_cell(0, 10, clean_line)
            
    # Output to a temporary file and read bytes
    return pdf.output(dest='S').encode('latin-1')
