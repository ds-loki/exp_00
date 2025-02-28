from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama

app = FastAPI()
llm = Llama(model_path="/app/mistral.gguf")  # Load GGUF model

@app.get("/health")
async def health():
    return {"status": "OK"}

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

@app.post("/generate")
async def generate(request: GenerateRequest):
    return {"prompt": request.prompt, "max_tokens": request.max_tokens}
