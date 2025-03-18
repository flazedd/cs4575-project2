import deepspeed
import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer

model = AutoModelForQuestionAnswering.from_pretrained('distilbert-base-uncased')
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')

# Use DeepSpeed for optimized inference
model = deepspeed.init_inference(model, mp_size=1, dtype=torch.float16)

context = "France is a country located in Western Europe. Its capital is Paris."
question = "What is the capital of France?"

inputs = tokenizer(question, context, return_tensors="pt")
outputs = model(**inputs)
answer = tokenizer.decode(outputs['start_logits'], outputs['end_logits'])

print(f"Answer: {answer}")
