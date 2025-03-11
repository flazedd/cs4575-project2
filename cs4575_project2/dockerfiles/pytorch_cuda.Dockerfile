FROM pytorch/pytorch:2.6.0-cuda11.8-cudnn9-devel

# Set the working directory inside the container
WORKDIR /app

# Copy the PyTorch training script into the container
COPY train_model.py .

# Set the command to run the training script
CMD ["python", "train_model.py"]
