# run_manager.py
import json
from manager_agent import ManagerAgent
from llm_wrappers import genai_call

# 1. SETUP THE MANAGER
# We increase max_output_tokens to 2000 so it can write the full plan.
# We explicitly use "gemini-1.5-flash" (or "gemini-pro") to avoid 404 errors.
manager = ManagerAgent(
    llm_caller=lambda p: genai_call(
        p, 
        model="models/gemini-2.5-flash", 
        max_output_tokens=2000
    )
)

# 2. DEFINE THE IDEA
idea = input()

print(f"--- ASKING MANAGER TO PLAN: '{idea}' ---")

# 3. GET THE PLAN
plan = manager.plan_project(idea)

# 4. PRINT THE RESULT
if "plan" in plan:
    print("\nSUCCESS! Here is the plan:")
    print(json.dumps(plan, indent=2))
else:
    print("\nSOMETHING WENT WRONG:")
    print(plan)