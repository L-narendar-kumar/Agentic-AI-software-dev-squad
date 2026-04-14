# test_genai_simple.py
from llm_wrappers import genai_call

PROMPT = '''
You are an assistant. Return a single-line JSON only.
{"action":"test", "message":"hello world"}
'''

print("Calling Gemini (short test)...")
out = genai_call(PROMPT, model="models/gemini-2.5-pro", temperature=0.0, max_output_tokens=200)
print("RAW OUTPUT:")
print(out)
