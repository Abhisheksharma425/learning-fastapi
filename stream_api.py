import requests
import json

url = "http://127.0.0.1:8000/chat"
payload = {
    "messages": [{"role": "user", "content": "Write a short poem about coding."}],
    "model_name": "qwen4:3b" # Make sure this matches your 'ollama list'
}

# stream=True is important to handle the StreamingResponse!
response = requests.post(url, json=payload, stream=True)

print("Streaming response:")
for chunk in response.iter_content(chunk_size=None):
    if chunk:
        print(chunk.decode("utf-8"), end="", flush=True)