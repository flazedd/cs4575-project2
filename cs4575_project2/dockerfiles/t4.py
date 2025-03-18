import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Local model directory (where files are stored)
model_dir = "./models/mistral"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    torch_dtype=torch.float16,  # Use float16 for efficiency
    device_map="auto"  # Automatically select GPU if available
)

# Create text generation pipeline
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Take user input
prompt = input("Enter your prompt: ")

# Generate response
output = generator(prompt, max_length=200, temperature=0.7, top_p=0.9, do_sample=True)

# Print result
print("\nAI Response:\n", output[0]["generated_text"])
