# Use an official PyTorch image with CUDA support
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Set the working directory inside the container
WORKDIR /app

## Copy the local test.py script to the container
#COPY test.py /app/test.py
#
## Install any dependencies (if any, for example, if your script uses other libraries)
#RUN pip install --no-cache-dir -r requirements.txt || echo "No requirements.txt found"

# Run the Python script to check GPU name
CMD ["python", "/app/test.py"]
