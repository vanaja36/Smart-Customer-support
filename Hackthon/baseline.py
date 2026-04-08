import os
import json
from openai import OpenAI
from tasks import EasyTask, MediumTask, HardTask
from env import Action

def formulate_prompt(obs, step_count) -> str:
    prompt = f"Step: {step_count}\n"
    prompt += f"Observation: {obs.model_dump_json()}\n"
    prompt += """You are a customer support agent processing tickets.
Choose ONE action in JSON format.
Action Space Schema:
{
  "action_type": "classify" | "respond" | "close",
  "ticket_id": "T1",
  "text_content": "category_name or response_text"
}
Available Categories: login_issue, billing, account, technical, sales.
Note: You must first 'classify' a ticket, then 'respond' to it, and finally 'close' it perfectly in that order.
Return ONLY valid JSON. No markdown backticks.
"""
    return prompt

def run_task(task_idx, task):
    print(f"\n--- Running Task {task_idx} ---")
    
    # Try to read HF_TOKEN from environment variables
    hf_token = os.environ.get("HF_TOKEN")
    
    # If the token is available, we query Hugging Face Inference API, otherwise fallback to local mock testing
    use_mock = False
    if hf_token:
        client = OpenAI(
            base_url="https://api-inference.huggingface.co/v1/",
            api_key=hf_token
        )
    else:
        print("Warning: HF_TOKEN not set. Running with a rule-based MOCK AI agent for demonstration.")
        use_mock = True
        
    env = task.env
    obs = env.reset()
    done = False
    
    while not done:
        prompt = formulate_prompt(obs, env.step_count)
        try:
            if use_mock:
                # Hardcoded demo rule-based agent to prove the environment works without an API key
                t = next((t for t in obs.open_tickets), None)
                if t:
                    if not t.category:
                        cat = "login_issue" if "password" in t.message.lower() else "billing" if "refund" in t.message.lower() or "charge" in t.message.lower() else "account" if "address" in t.message.lower() else "technical" if "crash" in t.message.lower() else "sales"
                        content = json.dumps({"action_type": "classify", "ticket_id": t.id, "text_content": cat})
                    elif not t.response:
                        content = json.dumps({"action_type": "respond", "ticket_id": t.id, "text_content": "This is a helpful support response covering your issue."})
                    else:
                        content = json.dumps({"action_type": "close", "ticket_id": t.id})
                else:
                    content = json.dumps({"action_type": "wait", "ticket_id": "unknown"})
            else:
                response = client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3-8B-Instruct",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=150,
                    temperature=0.1
                )
                content = response.choices[0].message.content.strip()
                
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            elif content.startswith("```"):
                content = content.replace("```", "").strip()
                
            act_dict = json.loads(content)
            action = Action(**act_dict)
        except Exception as e:
            print(f"Agent error (fallback to safe wait): {e}")
            action = Action(action_type="wait", ticket_id="unknown")
            
        print(f"Action taken: {action.model_dump_json()}")
        obs, reward, done, info = env.step(action)
        print(f"Reward: {reward.value} | Reason: {reward.reason}")
        
    score = task.evaluate(env)
    print(f"Task {task_idx} Completed with Score (0.0 to 1.0): {score}")
    return score

if __name__ == "__main__":
    tasks = [EasyTask(), MediumTask(), HardTask()]
    for i, t in enumerate(tasks):
        run_task(i + 1, t)
