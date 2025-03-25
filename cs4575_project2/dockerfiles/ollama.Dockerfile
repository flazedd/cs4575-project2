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

# Create working directory
WORKDIR /app

# Copy your script and start script
COPY ollama_library.py .
COPY start.sh .

# Make the start script executable
RUN chmod +x /app/start.sh

# Create directories
RUN mkdir -p /app/dataset /app/results

# Expose the Ollama API port
EXPOSE 11434
ENTRYPOINT ["/app/start.sh"]