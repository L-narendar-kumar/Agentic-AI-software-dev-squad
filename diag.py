# diag.py
import importlib, sys, json, os

print("Python executable:", sys.executable)
print("CWD:", os.getcwd())
print("--- try import google.generativeai ---")
try:
    import google.generativeai as genai_old
    print("google.generativeai imported. type:", type(genai_old))
    attrs = [a for a in dir(genai_old) if not a.startswith('_')]
    print("sample attrs:", attrs[:60])
except Exception as e:
    print("google.generativeai import error:", repr(e))

print("\n--- try import google.genai ---")
try:
    from google import genai as genai_new
    print("google.genai imported. type:", type(genai_new))
    attrs = [a for a in dir(genai_new) if not a.startswith('_')]
    print("sample attrs:", attrs[:60])
except Exception as e:
    print("google.genai import error:", repr(e))
