from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import ollama # Import the library

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

# --- Define Input for LLM ---
class PromptInput(BaseModel):
    prompt: str
    model_name: str = "qwen3:4b" # Default model

@app.post("/generate")
def generate_text(input_data: PromptInput):
    client = ml_resources.get("ollama")
    
    if not client:
        raise HTTPException(status_code=503, detail="Ollama service unavailable")

    # Call Ollama
    try:
        response = client.chat(model=input_data.model_name, messages=[
            {
                'role': 'user',
                'content': input_data.prompt,
            },
        ])
        return {"response": response['message']['content']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))