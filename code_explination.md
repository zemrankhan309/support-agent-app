# Code Explanation — Customer Support Intelligence App

This document explains how the project works internally, focusing on architecture, data flow, and key components.

---

# 🧱 Architecture Overview

The app follows a clean, modular structure:

UI (Streamlit)  →  LLM Client  →  OpenAI API
↑
Utilities


Each layer has a single responsibility:

- **app.py** — UI, layout, user interactions  
- **llm_client.py** — LLM wrapper, message building, retries, error handling  
- **utils.py** — helper functions  
- **secrets.toml** — API key (never committed)  

---

# 📘 app.py — Streamlit UI

### Responsibilities
- Render the sidebar (model, temperature, max tokens, system prompt)
- Render the chat interface
- Display insights (message count, summary, suggested actions)
- Call `LLMClient.generate_response()`
- Handle user input and maintain session state

### Flow
1. User enters a message  
2. Streamlit stores it in `st.session_state`  
3. UI calls the LLM client  
4. Response is displayed  
5. Insights panel updates  

---

# 🤖 llm_client.py — LLM Wrapper

### Responsibilities
- Initialize OpenAI client (`OpenAI(api_key=...)`)
- Build message list (system + history + user)
- Call the API using the new OpenAI SDK
- Handle retries (tenacity)
- Catch and surface errors cleanly

### Key Method: `generate_response()`

Steps:
1. Build messages  
2. Call `_call_openai()`  
3. If successful → return content  
4. If error → log traceback + return safe UI message  

### Error Handling
Catches:
- `RateLimitError`  
- `AuthenticationError`  
- `InvalidRequestError`  
- `OpenAIError`  
- Generic exceptions  

---

# 🔌 OpenAI SDK (v2.x)

The app uses:

```python
from openai import OpenAI
client = OpenAI(api_key=...)


Each layer has a single responsibility:

- **app.py** — UI, layout, user interactions  
- **llm_client.py** — LLM wrapper, message building, retries, error handling  
- **utils.py** — helper functions  
- **secrets.toml** — API key (never committed)  

---

# 📘 app.py — Streamlit UI

### Responsibilities
- Render the sidebar (model, temperature, max tokens, system prompt)
- Render the chat interface
- Display insights (message count, summary, suggested actions)
- Call `LLMClient.generate_response()`
- Handle user input and maintain session state

### Flow
1. User enters a message  
2. Streamlit stores it in `st.session_state`  
3. UI calls the LLM client  
4. Response is displayed  
5. Insights panel updates  

---

# 🤖 llm_client.py — LLM Wrapper

### Responsibilities
- Initialize OpenAI client (`OpenAI(api_key=...)`)
- Build message list (system + history + user)
- Call the API using the new OpenAI SDK
- Handle retries (tenacity)
- Catch and surface errors cleanly

### Key Method: `generate_response()`

Steps:
1. Build messages  
2. Call `_call_openai()`  
3. If successful → return content  
4. If error → log traceback + return safe UI message  

### Error Handling
Catches:
- `RateLimitError`  
- `AuthenticationError`  
- `InvalidRequestError`  
- `OpenAIError`  
- Generic exceptions  

---

# 🔌 OpenAI SDK (v2.x)

The app uses:

```python
from openai import OpenAI
client = OpenAI(api_key=...)


Each layer has a single responsibility:

- **app.py** — UI, layout, user interactions  
- **llm_client.py** — LLM wrapper, message building, retries, error handling  
- **utils.py** — helper functions  
- **secrets.toml** — API key (never committed)  

---

# 📘 app.py — Streamlit UI

### Responsibilities
- Render the sidebar (model, temperature, max tokens, system prompt)
- Render the chat interface
- Display insights (message count, summary, suggested actions)
- Call `LLMClient.generate_response()`
- Handle user input and maintain session state

### Flow
1. User enters a message  
2. Streamlit stores it in `st.session_state`  
3. UI calls the LLM client  
4. Response is displayed  
5. Insights panel updates  

---

# 🤖 llm_client.py — LLM Wrapper

### Responsibilities
- Initialize OpenAI client (`OpenAI(api_key=...)`)
- Build message list (system + history + user)
- Call the API using the new OpenAI SDK
- Handle retries (tenacity)
- Catch and surface errors cleanly

### Key Method: `generate_response()`

Steps:
1. Build messages  
2. Call `_call_openai()`  
3. If successful → return content  
4. If error → log traceback + return safe UI message  

### Error Handling
Catches:
- `RateLimitError`  
- `AuthenticationError`  
- `InvalidRequestError`  
- `OpenAIError`  
- Generic exceptions  

---

# 🔌 OpenAI SDK (v2.x)

The app uses:

```python
from openai import OpenAI
client = OpenAI(api_key=...)

AND Calls

client.chat.completions.create(
    model=config.model,
    messages=messages,
    temperature=config.temperature,
    max_tokens=config.max_tokens,
)

test_openai_quick.py
A minimal script to verify:

API key is loaded

Network connectivity

Model availability

SDK installation

This script isolates issues outside Streamlit.

🧰 utils.py
Contains helper functions such as:

formatting

message history handling

text cleaning

🔐 Secrets Management
secrets.toml is used for local development:

toml
OPENAI_API_KEY = "sk-..."
It is ignored by git to prevent leaks.

On Streamlit Cloud, secrets are stored in the Secrets Manager.

🧭 Data Flow Diagram
Code
User Input
    ↓
Streamlit UI (app.py)
    ↓
LLMClient.generate_response()
    ↓
OpenAI API (chat.completions)
    ↓
Response returned
    ↓
UI renders output + insights
🛡️ Reliability Features
Exponential backoff for rate limits

Clear error messages in UI

Full traceback logging in terminal

Model fallback capability

Configurable temperature and token limits

📌 Summary
This project is structured for:

Clean separation of concerns

Easy debugging

Safe secret handling

Compatibility with OpenAI’s new SDK

Extendability (embeddings, RAG, ticket classification, etc.)

Code

---

