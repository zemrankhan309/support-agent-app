# tests/test_openai_newsdk.py
import os, traceback
from openai import OpenAI

key = os.getenv("OPENAI_API_KEY")
print("OPENAI_API_KEY present:", bool(key))

try:
    client = OpenAI(api_key=key)
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello from new SDK test"}],
    )
    print("New SDK OK, response length:", len(resp.choices[0].message.content))
except Exception as e:
    print(type(e).__name__, str(e))
    traceback.print_exc()
