# todo_agent.py
from agent_base import AgentBase

PROMPT_TEMPLATE = '''
You are a tiny assistant that reads a single-line user command and returns JSON only.

Input command: "{user_command}"

Return exactly one JSON object, no commentary, no surrounding text, no markdown fences.
Allowed outputs:

1) Add:
{{"action":"add","text":"<todo text>"}}

2) List:
{{"action":"list"}}

3) Remove:
{{"action":"remove","index":<0-based integer>}}

4) Unknown:
{{"action":"unknown","message":"<short reason>"}}

EXAMPLE 1
Input command: "add buy eggs"
Output: {{"action":"add","text":"buy eggs"}}

EXAMPLE 2
Input command: "list"
Output: {{"action":"list"}}

Now produce the JSON for the Input command above.
'''

class ToDoAgent(AgentBase):
    def __init__(self, llm_caller):
        super().__init__(llm_caller)
        self.todos = []

    def handle_command(self, user_command: str):
        prompt = PROMPT_TEMPLATE.format(user_command=user_command.replace('"', '\\"'))
        raw = self.call_llm(prompt)

        # debug print (helpful while developing)
        print("DEBUG: raw llm output >>>")
        print(raw)
        print("DEBUG: end raw output <<<")

        # Parse JSON robustly
        try:
            parsed = self.parse_json(raw)
        except Exception as e:
            # Return a structured error so caller can handle (no crash)
            return {"status":"error", "message": f"Failed to parse LLM output: {e}", "raw": raw}

        if not isinstance(parsed, dict):
            return {"status":"error","message":"LLM returned non-object JSON","raw":raw}

        action = parsed.get("action")

        if action == "add":
            text = parsed.get("text")
            if not text:
                return {"status":"error","message":"Missing 'text' for add action", "raw":raw}
            self.todos.append(text)
            return {"status":"ok", "message": f'Added: \"{text}\"', "todos": list(self.todos)}

        if action == "list":
            return {"status":"ok", "todos": list(self.todos)}

        if action == "remove":
            idx = parsed.get("index")
            try:
                idx = int(idx)
                removed = self.todos.pop(idx)
                return {"status":"ok", "message": f'Removed: \"{removed}\"', "todos": list(self.todos)}
            except Exception as e:
                return {"status":"error","message": f"Invalid index: {e}", "raw": raw}

        return {"status":"error","message":"Unknown action", "raw": raw}
