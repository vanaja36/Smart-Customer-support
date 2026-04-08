# 🤖 Smart Customer Support OpenEnv

An AI-powered customer support simulation environment built for the Meta OpenEnv Hackathon. This project models real-world customer support workflows where an intelligent agent processes support tickets step-by-step.

---

## 🚀 Overview

This environment simulates how customer support agents:

- Classify incoming tickets  
- Generate meaningful responses  
- Resolve and close issues  

The system is designed to train and evaluate AI agents using structured observations, actions, and rewards.

---

## 🧠 Key Features

- ✅ Real-world task simulation (customer support)
- ✅ Structured OpenEnv environment
- ✅ Step-by-step agent decision making
- ✅ Reward-based evaluation system
- ✅ Supports both:
  - Hugging Face LLM (LLaMA 3)
  - Rule-based mock agent (fallback)

---

## 🏗️ Project Structure
├── baseline.py # Main agent runner
├── env.py # Environment logic
├── tasks.py # Task definitions (Easy, Medium, Hard)
├── requirements.txt # Dependencies
├── Dockerfile # Deployment configuration
└── README.md # Project documentation


---

## ⚙️ How It Works

### 🔹 Observation Space
- Open tickets
- Last action feedback

### 🔹 Action Space
```json
{
  "action_type": "classify | respond | close",
  "ticket_id": "T1",
  "text_content": "category or response"
}

🔹 Workflow
Classify ticket
Respond to ticket
Close ticket

🎯 Tasks
Difficulty	Description
Easy	Single login issue
Medium	Billing & account issues
Hard	Mixed complex tickets

Each task is evaluated with a score between 0.0 → 1.0

🏆 Reward System
✔ Correct classification → +0.2
✔ Good response → +0.3
✔ Successful closure → +0.5
❌ Wrong actions → penalty
▶️ Run Locally
1. Install dependencies
pip install -r requirements.txt
2. Run the agent
python baseline.py
🔐 Environment Variable

Set your Hugging Face token:

export HF_TOKEN=your_hf_token
🐳 Docker Setup
docker build -t smart-support .
docker run -e HF_TOKEN=your_hf_token smart-support
☁️ Deployment

This project is deployed using Hugging Face Spaces (Docker-based).

🤝 Use Cases
AI agent training
Reinforcement learning environments
Customer support automation research
Hackathon projects
💡 Future Improvements
Add UI (Gradio / Streamlit)
Multi-agent collaboration
Real-time chat interface
Advanced NLP evaluation metrics
👩‍💻 Author

Vanaja P
Aspiring AI Engineer 🚀
