# Use Python Bookworm as the base image
FROM python:3.12-bookworm

# Install Git LFS
RUN apt-get update && \
    apt-get install -y git-lfs && \
    git lfs install && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the default command to open an interactive shell
CMD ["/bin/bash"]