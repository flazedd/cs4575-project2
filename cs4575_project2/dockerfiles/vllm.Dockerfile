# Use Python 3.11.11 using Debian Bookworm
FROM python:3.11.11-bookworm

# Set the working directory inside the container
WORKDIR /app

# Install vllm==0.7.3 directly
RUN pip install --no-cache-dir vllm==0.7.3

# Copy the vllm inference library script into the container
COPY vllm_library.py ./

# Set the command to run the inference script
CMD ["python", "vllm_library.py"]