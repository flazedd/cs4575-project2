# Use Python 3.11.11 using Debian Bookworm
FROM python:3.11.11-bookworm

# # Set environment variables
# ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir \
    torch \
    transformers \
    accelerate \
    sentencepiece \
    pandas \
    numpy \
    tqdm \
    safetensors \
    ollama \
    requests

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

# Copy files
COPY ollama_library.py /app
COPY start.sh /app
COPY ../../datasets/SWE-bench_Lite_oracle.csv /app/dataset/dataset.csv
COPY ../../dockerfiles/run_inference.py /app/dockerfiles/run_inference.py
COPY ../../utils/prompt.py /app/utils/prompt.py

# Permissions
RUN chmod +x /app/start.sh

# Prepare result directory
RUN mkdir -p /app/results

EXPOSE 11434

ENTRYPOINT ["/app/start.sh"]