# Use Python 3.11.11 using Debian Bookworm
FROM python:3.11.11-bookworm

# Set which inference library file to use, default is vllm
ARG inference_library=vllm
ENV inference_library=${inference_library}

# Set the working directory inside the container
WORKDIR /app

# Install the application dependencies
COPY requirements_${inference_library}.txt ./
RUN pip install --no-cache-dir -r requirements_${inference_library}.txt

# Copy the inference library script into the container
COPY ${inference_library}_library.py ./

# Set the command to run the training script using a shell for variable expansion
CMD ["sh", "-c", "python ${inference_library}_library.py"]