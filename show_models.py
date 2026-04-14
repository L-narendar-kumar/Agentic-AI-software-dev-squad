# check_models.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found in environment.")
else:
    genai.configure(api_key=api_key)
    print("Checking available models for your API key...\n")
    try:
        found_any = False
        for m in genai.list_models():
            # We only care about models that can generate text/content
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
                found_any = True
        
        if not found_any:
            print("\nNo content generation models found. Check your API key permissions.")
            
    except Exception as e:
        print(f"Error listing models: {e}")