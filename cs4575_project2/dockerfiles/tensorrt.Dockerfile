FROM python:3.10.16-bookworm

# Define a cache key based on the CUDA version and Debian version
# ARG CUDA_VERSION=12.8.1
# ARG CUDA_SHORT=12-8
# ARG DEBIAN_VERSION=12

# Set the working directory inside the container
WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip setuptools

# Install libopenmpi
RUN apt-get -y install libopenmpi-dev

# # Download the CUDA repository package
# RUN wget https://developer.download.nvidia.com/compute/cuda/${CUDA_VERSION}/local_installers/cuda-repo-debian${DEBIAN_VERSION}-${CUDA_SHORT}-local_${CUDA_VERSION}-570.124.06-1_amd64.deb
# # Install the CUDA repository package
# RUN dpkg -i cuda-repo-debian${DEBIAN_VERSION}-${CUDA_SHORT}-local_${CUDA_VERSION}-570.124.06-1_amd64.deb
# # Copy the CUDA keyring
# RUN cp /var/cuda-repo-debian${DEBIAN_VERSION}-${CUDA_SHORT}-local/cuda-*-keyring.gpg /usr/share/keyrings/
# # Update the package list
# RUN apt-get update
# # Install the CUDA toolkit
# RUN apt-get -y install cuda-toolkit-${CUDA_SHORT}

# Install tensorrt-llm
RUN pip install tensorrt-llm --extra-index-url https://pypi.nvidia.com
RUN pip install autoawq

# Copy the inference library script into the container
# COPY tensorrt_library.py ./

# Set the command to run the training script using a shell for variable expansion
CMD ["python", "tensorrt_library.py"]