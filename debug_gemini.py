# debug_gemini.py
import sys
import google.generativeai as genai
import os

print(f"Python Executable: {sys.executable}")

try:
    print(f"Library Version: {genai.__version__}")
    print(f"Library File: {genai.__file__}")
except AttributeError:
    print("Could not determine version/file.")

# Check for the key functions
methods = [m for m in dir(genai) if "generate" in m]
print(f"\nAvailable generation methods: {methods}")

if "generate_content" in methods:
    print("\nSUCCESS: 'generate_content' is found. The library is up to date.")
else:
    print("\nFAILURE: 'generate_content' is MISSING. The library is old or shadowed.")