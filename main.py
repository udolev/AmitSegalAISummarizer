import google.generativeai as genai

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access Google API key using os.environ
google_api_key = os.environ.get('GOOGLE_API_KEY')

# Check if API key is loaded
if google_api_key is None:
    raise ValueError("Google API Key not found in .env file. Please set the 'GOOGLE_API_KEY' environment variable.")

genai.configure(api_key=google_api_key)

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("What is the meaning of life?")
print(response.text)