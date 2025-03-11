FROM pytorch/pytorch:latest
# Set the working directory inside the container
WORKDIR /app

# Copy the PyTorch training script into the container
COPY train_model.py .

# Set the command to run the training script
CMD ["python", "train_model.py"]
