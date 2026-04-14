# developer_agent.py
from agent_base import AgentBase

# UPDATED PROMPT: No JSON, just code.
DEV_PROMPT = '''
You are a Senior Software Developer.
Your task is to write the COMPLETE code for a single file based on these instructions.

File Name: "{file_name}"
Instructions: "{description}"

Output Format:
- Return ONLY the valid code.
- Do not include explanations or conversation.
- Wrap the code in standard markdown blocks (e.g. ```python ... ```).
'''

class DeveloperAgent(AgentBase):
    def write_code(self, file_name: str, description: str):
        # 1. Fill the template
        prompt = DEV_PROMPT.format(
            file_name=file_name, 
            description=description
        )
        
        # 2. Call Gemini
        print(f"DEBUG: Developer is writing code for '{file_name}'...")
        # call_llm automatically strips the ```markdown fences for us!
        code = self.call_llm(prompt)
        
        # 3. Return the raw code directly (No JSON parsing needed)
        return code 