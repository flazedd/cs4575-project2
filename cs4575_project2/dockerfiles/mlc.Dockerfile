FROM python:3.11.11-bookworm

# Download and install the CUDA keyring package
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/debian12/x86_64/cuda-keyring_1.1-1_all.deb && \
    dpkg -i cuda-keyring_1.1-1_all.deb && \
    rm cuda-keyring_1.1-1_all.deb
# Update apt and install the CUDA Toolkit 12.3
RUN apt-get update && \
    apt-get -y install cuda-toolkit-12-3 && \
    rm -rf /var/lib/apt/lists/*

# Install git-lfs
RUN apt-get update && \
    apt-get install -y git-lfs && \
    rm -rf /var/lib/apt/lists/*

# Add CUDA 12.3 to PATH and LD_LIBRARY_PATH
ENV PATH=/usr/local/cuda-12.3/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda-12.3/lib64:${LD_LIBRARY_PATH}

# Set the working directory inside the container
WORKDIR /app

# Install the MLC packages directly
RUN pip install --no-cache-dir --pre -U -f https://mlc.ai/wheels mlc-llm-nightly-cu123 mlc-ai-nightly-cu123

# Copy the MLC inference library script into the container
COPY mlc_library.py ./

# Set the command to run the inference script
CMD ["python", "mlc_library.py"]