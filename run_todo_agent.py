# run_todo_agent.py
from todo_agent import ToDoAgent
from llm_wrappers import genai_call

def run_with_gemini():
    agent = ToDoAgent(llm_caller=lambda p: genai_call(p, model="models/gemini-2.5-flash", temperature=0.0, max_output_tokens=300))
    print("Running ToDoAgent with GEMINI. Type 'quit' to exit.")
    while True:
        cmd = input(">>> ").strip()
        if not cmd:
            continue
        if cmd.lower() in ("quit", "exit"):
            print("bye")
            break
        out = agent.handle_command(cmd)
        print(out)

if __name__ == "__main__":
    run_with_gemini()
