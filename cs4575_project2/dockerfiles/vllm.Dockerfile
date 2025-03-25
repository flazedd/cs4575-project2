# Use Python 3.10.16 using Debian Bookworm
FROM python:3.10.16-bookworm

# Set the working directory inside the container
WORKDIR /app

# Install vllm==0.7.3 directly
RUN pip install --no-cache-dir vllm==0.7.3 pandas

# # Copy the vllm inference library script into the container
# COPY vllm_library.py ./
# # Copy datasets directory into container
# COPY datasets/ ./
# # Copy model into container
# COPY Qwen2.5-1.5B-Instruct-AWQ ./

# Set the command to run the inference script
CMD ["python", "vllm_library.py"]