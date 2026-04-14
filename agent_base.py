# agent_base.py
import json
import re

def clean_code_block(s: str) -> str:
    """
    Remove surrounding markdown code fences (```...```) if present,
    and trim whitespace. Keeps inner content unchanged.
    """
    return re.sub(r"^```[\w]*\n|```$", "", s.strip(), flags=re.M)


class AgentBase:
    """
    Minimal base class for agents.

    Agents should be given an llm_caller: a callable that accepts a prompt
    string and returns the LLM's response (string or dict-like).
    """

    def __init__(self, llm_caller):
        if not callable(llm_caller):
            raise TypeError("llm_caller must be a callable that accepts a prompt string")
        self.llm = llm_caller

    def call_llm(self, prompt: str) -> str:
        """
        Call the injected LLM caller and normalize the result to a plain string.

        Accepts:
          - functions that return a plain string
          - functions that return a dict-like object with keys like 'text'/'content'
          - wrappers that return an SDK response object (we call str() as fallback)

        Always returns a cleaned string (no triple-backtick fences).
        """
        raw = self.llm(prompt)

        # If the wrapper returns a mapping-like object, try common keys:
        if isinstance(raw, dict):
            text = raw.get("content") or raw.get("text") or raw.get("output") or str(raw)
        else:
            # Could be an SDK object; convert to string
            text = str(raw)

        return clean_code_block(text)

    def parse_json(self, text: str):
        """
        Robustly extract and parse the first JSON object/array found in `text`.

        - If the entire text is valid JSON -> parse it directly.
        - Otherwise search for the first {...} or [...] block and parse that.
        - Raises RuntimeError if no JSON found or JSON is invalid.
        """
        text = (text or "").strip()
        if not text:
            raise RuntimeError("parse_json: input text is empty or None")

        # Try direct parse first
        try:
            return json.loads(text)
        except Exception:
            pass

        # Extract first {...} or [...] block (DOTALL so . matches newline)
        m = re.search(r"(\{(?:.|\n)*?\}|\[(?:.|\n)*?\])", text, flags=re.S)
        if not m:
            # show a helpful snippet so debugging is easier
            snippet = text[:400] + ("..." if len(text) > 400 else "")
            raise RuntimeError(f"parse_json: No JSON found in LLM output. Raw (truncated):\n{snippet}")

        block = m.group(1)
        try:
            return json.loads(block)
        except Exception as e:
            raise RuntimeError(f"parse_json: Found JSON-like block but failed to parse. Block:\n{block}\n\nError: {e}") from e
