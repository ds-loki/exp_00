from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
from starlette.concurrency import run_in_threadpool

app = FastAPI()
# Load your Mistral GGUF model (make sure this file is present at /app/mistral.gguf)
llm = Llama(model_path="/app/mistral.gguf")

@app.get("/health")
async def health():
    return {"status": "OK"}

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

@app.post("/generate")
async def generate(request: GenerateRequest):
    # Format the prompt using the proper Mistral Instruct format:
    # Wrap the instruction in <s>[INST] ... [/INST]
    formatted_prompt = f"<s>[INST] {request.prompt.strip()} [/INST]"
    
    # Call the blocking llama_cpp function in a thread pool
    output = await run_in_threadpool(llm, formatted_prompt, max_tokens=request.max_tokens)
    
    # Extract response text, stopping at the EOS token if present
    if "choices" in output and len(output["choices"]) > 0:
        response_text = output["choices"][0]["text"].strip().split("</s>")[0]
        return {"response": response_text}
    
    return {"response": "No output generated."}
