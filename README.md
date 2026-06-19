# Customer Support Intelligence (LLM-Powered Support Agent)

An AI-powered customer support assistant built with **Streamlit**, **OpenAI**, and a modular Python backend.  
This tool helps support agents summarize tickets, generate responses, extract insights, and accelerate customer communication.

---

## 🚀 Features

- Chat interface for asking questions, summarizing tickets, or generating replies  
- LLM configuration panel (model, temperature, max tokens, system prompt)  
- Insights panel showing message count, suggested actions, and ticket summary  
- Modular architecture with clean separation of UI, LLM client, and utilities  
- Supports OpenAI’s new Python SDK (`openai>=2.x`)  
- Graceful error handling for rate limits, invalid keys, and network issues  

---

## 📦 Project Structure

support-agent-app/
│
├── app.py                     # Streamlit UI
├── llm_client.py              # LLM wrapper using OpenAI SDK
├── utils.py                   # Helper functions
├── requirements.txt           # Python dependencies
├── test_openai_quick.py       # Minimal API connectivity test
│
└── .streamlit/
└── secrets.toml           # API key (ignored by git)


---

## 🔧 Installation

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/support-agent-app.git
cd support-agent-app


---

## 🔧 Installation

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/support-agent-app.git
cd support-agent-app

# Create envoirnment 
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\Activate.ps1  # Windows PowerShell

# Install Dependencies
pip install -r requirements.txt

# Configure API Key
.streamlit/secrets.toml
OPENAI_API_KEY = "sk-your-key-here"

 Never commit this file. It is already in .gitignore

 streamlit run app.py

http://localhost:8501

🛡️ Error Handling
The app gracefully handles:

Missing or invalid API key

Rate limits (429)

Billing/quota exhaustion

Model availability issues

Network connectivity problems



🤝 Contributing
Pull requests are welcome.
For major changes, open an issue first to discuss what you’d like to modify.

⭐ Acknowledgements
Streamlit

OpenAI

<img width="1915" height="962" alt="image" src="https://github.com/user-attachments/assets/320f6a24-5158-4c93-8a4c-9f570da80eff" />



Python community




