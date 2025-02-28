FROM ubuntu:22.04  

WORKDIR /app  

# Install dependencies  
RUN apt update && apt install -y git g++ cmake make python3 python3-pip wget ninja-build dos2unix  pydantic

# Clone and build llama.cpp  
RUN git clone https://github.com/ggerganov/llama.cpp.git  
WORKDIR /app/llama.cpp  
RUN cmake . && make -j4  

# Install Python dependencies  
RUN pip3 install fastapi uvicorn llama-cpp-python  

# Download GGUF model  
WORKDIR /app  
RUN wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf -O mistral.gguf  

# Copy files  
COPY api.py /app/api.py  
COPY run.sh /app/run.sh  

# Fix line endings and make script executable  
RUN dos2unix /app/run.sh && chmod +x /app/run.sh  

# Expose API port  
EXPOSE 8080  

# Run script  
CMD ["/app/run.sh"]
