from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama

app = FastAPI(title="On-Demand AI API")

class PromptInput(BaseModel):
    prompt: str
    model_name: str = "qwen3:4b" 

@app.post("/generate")
def generate_text(input_data: PromptInput):
    print(f"Request received. Loading {input_data.model_name} from disk (this will be slow)...")
    
    try:
        # --- THE KEY PART ---
        # keep_alive=0 tells Ollama: "Unload model immediately after response"
        response = ollama.chat(
            model=input_data.model_name, 
            messages=[{'role': 'user', 'content': input_data.prompt}],
            keep_alive=0 
        )
        
        print("Response sent. Model unloaded from memory.")
        return {"response": response['message']['content']}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)