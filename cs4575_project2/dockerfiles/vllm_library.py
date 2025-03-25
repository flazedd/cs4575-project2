from vllm import LLM
import time
import pandas as pd

# Configuration
# MODEL = "Qwen2.5-1.5B-Instruct-q4f16_1-MLC"
# MMLU_PATH = "datasets/mmlu_stem_subset.csv"
MODEL = "volume/Qwen2.5-1.5B-Instruct-AWQ"  # Local path to the model
MMLU_PATH = "volume/datasets/mmlu_stem_subset.csv"  # CSV file with a "question" column

# Create vLLM instance
llm = LLM(
    model=MODEL,
    device="cuda",          # Use NVIDIA GPU
    quantization="awq",     # AWQ 4-bit quantization
    max_model_len=16384,    # Decrease context window to 16384 tokens
)

# Load the MMLU dataset; ensure the CSV has a column named "question"
df = pd.read_csv(MMLU_PATH)
token_metrics = []

# Set up sampling parameters
sampling_params = llm.get_default_sampling_params()
sampling_params.temperature = 0.0
sampling_params.max_tokens = 2048  # Maximum output tokens

# Iterate through the first 5 questions
for index, row in df.head(5).iterrows():
    question = row['question']
    prompt = question  # Customize the prompt if needed
    print(f"\nProcessing question {index}: {question}\n")
    
    # Time the generation call
    start_time = time.time()
    outputs = llm.generate(prompt, sampling_params)
    end_time = time.time()
    
    # Retrieve generated tokens from metadata (if available)
    generated_tokens = outputs[0].metadata['generated_tokens']
    total_time = end_time - start_time
    tokens_per_second = generated_tokens / total_time if total_time > 0 else 0

    # Extract and print the generated response
    response_text = outputs[0].outputs[0].text
    print("Response:\n", response_text)
    print(f"\nToken per second: {tokens_per_second:.2f}\n")
    
    # Save the metric for the current prompt
    token_metrics.append({
        "question_index": index,
        "token_per_sec": tokens_per_second
    })

# Save all token speed metrics to a CSV file
metrics_df = pd.DataFrame(token_metrics)
metrics_df.to_csv("token_sec_vllm.csv", index=False)

print("Experiment is done!")