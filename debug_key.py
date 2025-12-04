import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API Key NOT FOUND")
else:
    print(f"API Key Found. Length: {len(api_key)}")
    print(f"First 4 chars: {api_key[:4]}")
    print(f"Last 4 chars: {api_key[-4:]}")
    print(f"Repr: {repr(api_key)}")
    
    genai.configure(api_key=api_key.strip())
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello")
        print("API Call Successful")
    except Exception as e:
        print(f"API Call Failed: {e}")
