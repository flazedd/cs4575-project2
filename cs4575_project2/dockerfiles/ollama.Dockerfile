# Use Python 3.10.16 based on Debian Bookworm
FROM python:3.10.16-bookworm

# Set the working directory inside the container
WORKDIR /app

# Install Ollama CLI
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install Python dependencies
RUN pip install requests pandas ollama

# Expose the port used by Ollama service (if applicable)
EXPOSE 11434

# Set the default command to start Ollama service and run your inference script
CMD ["sh", "-c", "ollama serve & python ollama_library.py"]
