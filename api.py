from fastapi import FastAPI
from llama_cpp import Llama

app = FastAPI()
llm = Llama(model_path="/app/mistral.gguf")  # Load GGUF model

@app.get("/health")
async def health():
    return {"status": "OK"}

@app.post("/generate")
async def generate(prompt: str, max_tokens: int = 100):
    output = llm(prompt, max_tokens=max_tokens)
    return {"response": output["choices"][0]["text"]}
