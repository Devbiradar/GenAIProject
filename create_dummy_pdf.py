import fitz  # PyMuPDF

def create_dummy_pdf(output_path):
    doc = fitz.open()
    page = doc.new_page()
    
    text = """
    John Doe
    Email: john.doe@example.com
    Phone: (555) 123-4567
    
    Summary:
    Motivated software enthusiast with a passion for data and AI.
    
    Skills:
    Python, SQL, Machine Learning, Data Analysis, Git, Communication
    
    Experience:
    Junior Developer at Tech Corp (2022-Present)
    - Developed Python scripts for automation.
    - Worked with SQL databases.
    
    Education:
    B.S. in Computer Science, University of Tech (2018-2022)
    """
    
    page.insert_text((50, 50), text, fontsize=12)
    doc.save(output_path)
    print(f"Created dummy PDF at {output_path}")

if __name__ == "__main__":
    import os
    if not os.path.exists("data"):
        os.makedirs("data")
    create_dummy_pdf("data/sample_resume.pdf")
