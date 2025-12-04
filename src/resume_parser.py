import fitz  # PyMuPDF
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using PyMuPDF.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    return text

def parse_resume(text):
    """
    Parses raw text to extract structured information using Gemini.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not found. Falling back to basic regex parser (not implemented).")
        return {"raw_text": text, "error": "API Key missing"}

    genai.configure(api_key=api_key.strip())
    # Switching to gemini-2.0-flash as 1.5 versions were giving 404
    model = genai.GenerativeModel('gemini-2.0-flash')

    print(f"DEBUG: Extracted text length: {len(text)}")
    print(f"DEBUG: Extracted text preview: {text[:200]}...")

    prompt = f"""
    You are an expert Resume Parser. Extract the following information from the resume text below and return it as a valid JSON object.
    
    Resume Text:
    {text}
    
    Required Fields:
    - name (string)
    - email (string)
    - phone (string)
    - skills (list of strings)
    - education (list of objects with 'degree', 'institution', 'year')
    - experience (list of objects with 'role', 'company', 'duration', 'description')
    
    Return ONLY the JSON object. Do not include markdown formatting like ```json ... ```.
    """
    
    try:
        print("DEBUG: Sending request to Gemini...")
        response = model.generate_content(prompt)
        print("DEBUG: Response received.")
        # Clean response if it contains markdown code blocks
        cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
        print(f"DEBUG: Cleaned response text: {cleaned_text}")
        data = json.loads(cleaned_text)
        data["raw_text"] = text # Keep raw text for reference
        return data
    except Exception as e:
        print(f"Error parsing resume with Gemini: {e}")
        if 'response' in locals():
            print(f"Raw response: {response.text}")
        return {
            "raw_text": text,
            "error": str(e),
            "skills": [],
            "education": [],
            "experience": []
        }

if __name__ == "__main__":
    # Test with a dummy file if it exists
    test_pdf = "data/sample_resume.pdf"
    if not os.path.exists(test_pdf):
        # Try relative to src if running from src
        test_pdf = "../data/sample_resume.pdf"

    if os.path.exists(test_pdf):
        print(f"Extracting text from {test_pdf}...")
        extracted_text = extract_text_from_pdf(test_pdf)
        print("Extraction complete.")
        
        print("Parsing data with Gemini...")
        parsed_data = parse_resume(extracted_text)
        print("Parsed Data:", json.dumps(parsed_data, indent=2))
    else:
        print(f"No sample resume found for testing at {test_pdf}")
