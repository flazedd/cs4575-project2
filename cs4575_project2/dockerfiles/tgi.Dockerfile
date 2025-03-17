# Use Python 3.11.11 using Debian Bookworm
FROM python:3.11.11-bookworm

# Set the working directory inside the container
WORKDIR /app

RUN PROTOC_ZIP=protoc-21.12-linux-x86_64.zip && \
curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v21.12/$PROTOC_ZIP && \
unzip -o $PROTOC_ZIP -d /usr/local bin/protoc && \
unzip -o $PROTOC_ZIP -d /usr/local 'include/*' && \
rm -f $PROTOC_ZIP

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs

# Create a virtual environment using venv (this replaces the conda environment)
RUN python -m venv /app/venv

# Update PATH so that the venv’s Python and pip are used in subsequent commands
ENV PATH="/app/venv/bin:$PATH"

RUN export CUDA_HOME=/usr/local/cuda-1.24

RUN git clone https://github.com/huggingface/text-generation-inference.git && \
cd text-generation-inference && \
BUILD_EXTENSIONS=True make install