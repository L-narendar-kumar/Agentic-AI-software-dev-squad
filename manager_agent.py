# manager_agent.py
from agent_base import AgentBase

# THE INSTRUCTIONS (The "Brain" of the Manager)
MANAGER_PROMPT = '''
You are a Senior Technical Project Manager.
Your goal is to break down a software idea into 3-5 clear, implementable coding steps.

User Idea: "{user_idea}"

Output MUST be a single JSON object with this structure:
{{
  "plan": [
    {{
      "step": 1,
      "description": "Create the basic HTML structure...",
      "file_name": "index.html"
    }},
    {{
      "step": 2,
      "description": "Write the Python logic for...",
      "file_name": "app.py"
    }}
  ]
}}

Do not add any markdown formatting or extra text. Just the JSON.
'''

class ManagerAgent(AgentBase):
    def __init__(self, llm_caller):
        super().__init__(llm_caller)

    def plan_project(self, user_idea: str):
        # 1. Fill the template with the user's idea
        prompt = MANAGER_PROMPT.format(user_idea=user_idea.replace('"', '\\"'))
        
        # 2. Call the "Telephone" (Send to Gemini)
        print(f"DEBUG: Manager is thinking about '{user_idea}'...")
        raw_response = self.call_llm(prompt)
        
        # 3. Translate the messy string into a real Python Dictionary
        try:
            parsed = self.parse_json(raw_response)
            return parsed
        except Exception as e:
            return {"error": f"Manager failed to plan: {e}", "raw": raw_response}