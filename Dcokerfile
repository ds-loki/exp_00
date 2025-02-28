FROM ubuntu:22.04  

WORKDIR /app  

# Install dependencies  
RUN apt update && apt install -y git g++ cmake make python3 python3-pip wget  

# Install llama.cpp  
RUN git clone https://github.com/ggerganov/llama.cpp.git /app/llama.cpp  
WORKDIR /app/llama.cpp  
RUN make -j$(nproc)  

# Install Python packages  
RUN pip3 install fastapi uvicorn llama-cpp-python  

# Download GGUF model  
RUN wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf -O /app/mistral.gguf  

# Copy API script  
COPY api.py /app/api.py  

# Expose API port  
EXPOSE 8000  

# Run API  
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
