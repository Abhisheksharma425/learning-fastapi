from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import ollama # Import the library
from typing import List
from fastapi.responses import StreamingResponse
# --- Global Storage for the Client ---
ml_resources = {}

# --- The Lifespan (Ollama Version) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup: Connecting to Ollama...")
    
    # 1. Initialize the Client
    # Ollama usually runs on localhost:11434 by default
    client = ollama.Client(host='http://localhost:11434')
    
    try:
        # 2. "Health Check" the connection
        # We try to list models to ensure Ollama is actually running
        client.list()
        print("Success: Connected to Ollama server!")
        ml_resources["ollama"] = client
        print(ml_resources)
    except Exception as e:
        print(f"ERROR: Could not connect to Ollama. Is it running? {e}")
        # In a real app, you might want to stop the server here if AI is critical
    
    yield # App runs here
    
    # 3. Shutdown
    print("Shutdown: Closing connection resources...")
    ml_resources.clear()

app = FastAPI(lifespan=lifespan)

# # --- Define Input for LLM ---
# class PromptInput(BaseModel):
#     prompt: str
#     model_name: str = "qwen3:4b" # Default model

class Message(BaseModel):
    role: str
    content: str

class ChatInput(BaseModel):
    messages: List[Message]
    model_name: str = 'qwen3:4b'




@app.post("/chat")
def generate_text(input_data: ChatInput):
    client = ml_resources.get("ollama")

    def response_generator():
        stream = client.chat(model = input_data.model_name, messages = [msg.model_dump() for msg in input_data.messages], stream = True)
        for chunks in stream:
            yield chunks['message']['content']
    return StreamingResponse(response_generator(), media_type="text/plain")