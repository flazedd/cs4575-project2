# Use Python 3.11.11 using Debian Bookworm
FROM ubuntu:latest
# FROM python:3.11.11-bookworm

# Set which inference library file to use, default is vllm
ARG inference_library=tensorrt
ENV inference_library=${inference_library}

# Set the working directory inside the container
WORKDIR /app

# Install nvidia drivers
# RUN echo "deb http://ftp.au.debian.org/debian/ bookworm main non-free contrib non-free-firmware" > /etc/apt/sources.list
# RUN echo "deb-src http://ftp.au.debian.org/debian/ bookworm main non-free contrib non-free-firmware" >> /etc/apt/sources.list
RUN apt-get update && apt-get upgrade -y
# RUN apt install nvidia-driver firmware-misc-nonfree -y

# Install Python
RUN apt-get install python3-pip -y

# Install misc.
RUN apt-get -y install libopenmpi-dev
RUN apt install git -y

# RUN pip install --upgrade pip setuptools --break-system-packages

# Install tensorrt-llm
RUN pip install tensorrt-llm --extra-index-url https://pypi.nvidia.com --break-system-packages

# Copy the inference library script into the container
COPY ${inference_library}_library.py ./

# Set the command to run the training script using a shell for variable expansion
CMD ["sh", "-c", "python3 tensorrt_library.py"]