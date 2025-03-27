# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install required Python packages
RUN pip install docker torch

# Command to run the script inside the mounted volume
CMD ["python", "/app/test.py"]

# Use an appropriate base image (e.g., Python or CUDA base image)

