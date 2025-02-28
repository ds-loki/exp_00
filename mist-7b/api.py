import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_cpp import Llama
from starlette.concurrency import run_in_threadpool

app = FastAPI()
model_path = "/app/mistral.gguf"

# Check if the model file exists
if not os.path.isfile(model_path):
    raise RuntimeError(f"Model file not found: {model_path}. Ensure the file exists before running the API.")

llm = Llama(model_path=model_path)  # Load the model

@app.get("/health")
async def health():
    return {"status": "OK"}

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

@app.post("/generate")
async def generate(request: GenerateRequest):
    output = await run_in_threadpool(llm, request.prompt, max_tokens=request.max_tokens)

    if "choices" in output and len(output["choices"]) > 0:
        response_text = output["choices"][0]["text"].strip().split("</s>")[0]
        return {"response": response_text}

    return {"response": "No output generated."}
