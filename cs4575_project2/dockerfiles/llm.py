from transformers import pipeline
import torch
print(f'Getting generator...')
device = 0 if torch.cuda.is_available() else -1
print(f'device {device}')
# Initialize the pipeline with the appropriate device (GPU)
classifier = pipeline("sentiment-analysis", device=device)

# Test the classifier
result = classifier("This product is awful!")
print(result)