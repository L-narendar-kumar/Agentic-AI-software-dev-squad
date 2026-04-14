# agent_base.py
import json
import re

def clean_code_block(s: str) -> str:
    """
    Remove surrounding markdown code fences (```...```) if present,
    and trim whitespace.
    """
    if s is None:
        return ""
    return re.sub(r"^```[\w]*\n|```$", "", s.strip(), flags=re.M)

class AgentBase:
    """
    Minimal base class for agents.
    llm_caller: callable(prompt: str) -> str (must return text)
    """

    def __init__(self, llm_caller):
        if not callable(llm_caller):
            raise TypeError("llm_caller must be callable")
        self.llm = llm_caller

    def call_llm(self, prompt: str) -> str:
        """Call the injected LLM and return cleaned plain text."""
        raw = self.llm(prompt)
        if isinstance(raw, dict):
            text = raw.get("content") or raw.get("text") or raw.get("output") or str(raw)
        else:
            text = str(raw)
        return clean_code_block(text)

    def parse_json(self, text: str):
        """
        Robustly parse JSON returned by LLM.
        - tries direct json.loads(text)
        - otherwise finds first {...} or [...] block and parses it
        - raises RuntimeError with helpful text on failure
        """
        text = (text or "").strip()
        if not text:
            raise RuntimeError("parse_json: empty LLM output")

        # Try direct parse
        try:
            return json.loads(text)
        except Exception:
            pass

        # Find first JSON object/array
        m = re.search(r"(\{(?:.|\n)*?\}|\[(?:.|\n)*?\])", text, flags=re.S)
        if not m:
            snippet = text[:400] + ("..." if len(text) > 400 else "")
            raise RuntimeError(f"parse_json: No JSON found. Raw (truncated):\n{snippet}")

        block = m.group(1)
        try:
            return json.loads(block)
        except Exception as e:
            raise RuntimeError(f"parse_json: Found JSON-like block but failed to parse.\nBlock:\n{block}\n\nError: {e}") from e
