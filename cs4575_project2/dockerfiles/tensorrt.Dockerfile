# Use Python 3.11.11 using Debian Bookworm
# FROM ubuntu:latest
FROM python:3.11.11-bookworm

# Set which inference library file to use, default is vllm
ARG inference_library=tensorrt
ENV inference_library=${inference_library}

# Define a cache key based on the CUDA version and Debian version
ARG CUDA_VERSION=12.8.1
ARG CUDA_SHORT=12-8
ARG DEBIAN_VERSION=12

# Set the working directory inside the container
WORKDIR /app

# Install nvidia drivers
RUN apt-get update && apt-get upgrade -y

# Install misc.
RUN apt-get -y install libopenmpi-dev

# Download the CUDA repository package
RUN wget https://developer.download.nvidia.com/compute/cuda/${CUDA_VERSION}/local_installers/cuda-repo-debian${DEBIAN_VERSION}-${CUDA_SHORT}-local_${CUDA_VERSION}-570.124.06-1_amd64.deb
# Install the CUDA repository package
RUN dpkg -i cuda-repo-debian${DEBIAN_VERSION}-${CUDA_SHORT}-local_${CUDA_VERSION}-570.124.06-1_amd64.deb
# Copy the CUDA keyring
RUN cp /var/cuda-repo-debian${DEBIAN_VERSION}-${CUDA_SHORT}-local/cuda-*-keyring.gpg /usr/share/keyrings/
# Update the package list
RUN apt-get update
# Install the CUDA toolkit
RUN apt-get -y install cuda-toolkit-${CUDA_SHORT}

# Add CUDA 12.3 to PATH and LD_LIBRARY_PATH
ENV PATH=/usr/local/cuda-12.8/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64

# # Install misc.
# RUN apt-get -y install libopenmpi-dev
# RUN apt install git -y

RUN pip install --upgrade pip setuptools


RUN curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
RUN apt-get update
RUN apt-get install -y nvidia-container-toolkit

RUN nvidia-smi

# Install tensorrt-llm
RUN pip install tensorrt-llm --extra-index-url https://pypi.nvidia.com

# Copy the inference library script into the container
COPY ${inference_library}_library.py ./

# Set the command to run the training script using a shell for variable expansion
CMD ["sh", "-c", "nvidia-smi"]