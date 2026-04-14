# llm_wrappers.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def genai_call(prompt: str,
               model: str = "gemini-1.5-flash",
               temperature: float = 0.0,
               max_output_tokens: int = 300,
               debug: bool = True):
    """
    Modern wrapper for Google Gemini (Version 0.8.x+)
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return '{"action":"error","message":"Missing GOOGLE_API_KEY"}'

    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        return f'{{"action":"error","message":"Configuration failed: {e}"}}'

    try:
        # NEW STYLE: Create the model object first
        # We strip 'models/' prefix if user included it, as the SDK handles it
        clean_model_name = model.replace("models/", "")
        
        gemini_model = genai.GenerativeModel(
            model_name=clean_model_name,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens
            }
        )

        if debug:
            print(f"DEBUG: Calling model '{clean_model_name}'...")

        # Call generate_content
        response = gemini_model.generate_content(prompt)
        
        # Extract text safely
        if response.text:
            return response.text.strip()
        else:
            return '{"action":"error","message":"Model returned empty response"}'

    except Exception as e:
        # Return a JSON error string so the agent doesn't crash
        return f'{{"action":"error","message":"GenAI Call Failed: {str(e)}"}}'