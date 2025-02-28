from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
from starlette.concurrency import run_in_threadpool

app = FastAPI()
llm = Llama(model_path="/app/mistral.gguf")  # Ensure this file exists

@app.get("/health")
async def health():
    return {"status": "OK"}

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

@app.post("/generate")
async def generate(request: GenerateRequest):
    # Run the blocking model call in a thread pool
    output = await run_in_threadpool(llm, request.prompt, max_tokens=request.max_tokens)

    # Extract response text and stop at the EOS token if present
    if "choices" in output and len(output["choices"]) > 0:
        response_text = output["choices"][0]["text"].strip().split("</s>")[0]
        return {"response": response_text}

    return {"response": "No output generated."}
