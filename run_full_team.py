# run_full_team.py
import json
import os
from manager_agent import ManagerAgent
from developer_agent import DeveloperAgent
from llm_wrappers import genai_call

# --- CONFIGURATION ---
# Use the model name that works for you!
MY_MODEL = "models/gemini-2.5-flash"  # or "gemini-pro"

# 1. Initialize Agents
manager = ManagerAgent(llm_caller=lambda p: genai_call(p, model=MY_MODEL, max_output_tokens=8000))
developer = DeveloperAgent(llm_caller=lambda p: genai_call(p, model=MY_MODEL, max_output_tokens=10000))

# 2. Get User Idea
user_idea = input("Enter your project: ")
print(f"--- 1. PROJECT MANAGER: Planning '{user_idea}' ---")

plan = manager.plan_project(user_idea)

if "plan" not in plan:
    print("Error: Manager failed to create a plan.")
    print(plan)
    exit()

print("Plan accepted!")
print(json.dumps(plan, indent=2))

# 3. Execute Plan (The Loop)
print("\n--- 2. DEVELOPER: Starting work ---")

# Create a folder for the project output
output_folder = "project_output"
os.makedirs(output_folder, exist_ok=True)

for task in plan["plan"]:
    step = task.get("step")
    fname = task.get("file_name")
    desc = task.get("description")
    
    print(f"\n[Step {step}] Working on: {fname}...")
    print(f"   Instruction: {desc}")
    
    # Call the Developer Agent
    code = developer.write_code(fname, desc)
    
    # Save the file to disk
    file_path = os.path.join(output_folder, fname)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    
    print(f"   Saved to: {file_path}")

print("\n--- PROJECT COMPLETE ---")
print(f"Check the '{output_folder}' directory for your files!")