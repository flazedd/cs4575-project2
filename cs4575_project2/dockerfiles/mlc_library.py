from mlc_llm import MLCEngine
from mlc_llm.serve.config import EngineConfig
import pandas as pd

MODEL = "Qwen2.5-1.5B-Instruct-q4f16_1-MLC"
MMLU_PATH = "datasets/mmlu_stem_subset.csv"
# MMLU_PATH = "volume/datasets/mmlu_stem_subset.csv"
# MODEL = "volume/Qwen2.5-1.5B-Instruct-q4f16_1-MLC"

# Create engine model
model_engine = MLCEngine(
    model=MODEL,
    device="cuda",
    engine_config=EngineConfig(
        max_single_sequence_length=16384,  # Decrease context window by 50% (from 32768 default)
        prefill_chunk_size=1024), # Decrease chunk size by 50% (from 2048 default to 1024)
)
# Load the MMLU dataset; adjust the column name if necessary.
df = pd.read_csv(MMLU_PATH)
# List to store token per second metrics for each prompt.
token_metrics = []
# Iterate through each question in the dataset.
for index, row in df.head(5).iterrows():
    question = row['question']
    prompt = question  # You can customize this prompt if needed.
    
    print(f"Processing question {index}: {question}\n")
    
    # Send prompt to the MLC engine using streaming
    for response in model_engine.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=MODEL,
        stream=True,
        max_tokens=2048,  # Maximum tokens for output
        temperature=0.0,
    ):
        for choice in response.choices:
            # Print the streamed answer output
            print(choice.delta.content, end="", flush=True)
    print("\n")
    
    # Retrieve engine metrics after processing the prompt.
    metrics = model_engine.metrics()
    token_per_sec = metrics["decode_tokens_per_s"]
    print(f"Token per seconds: {token_per_sec}\n")
    
    # Save the metric for the current question.
    token_metrics.append({
        "question_index": index,
        "token_per_sec": token_per_sec
    })

# Save all token per second metrics to a CSV file.
metrics_df = pd.DataFrame(token_metrics)
metrics_df.to_csv("token_sec_mlc.csv", index=False)

print("Experiment is done, closing engine now")
model_engine.terminate()

# # Test prompt
# prompt = """
# You are interested in studying a rare type of breast cancer in a mouse model. 
# Your research up until now has shown that the cancer cells show low expression of a key tumor suppressor gene. 
# Which of these is the most suitable course of action to study the cause of gene silencing?
# """

# # Run chat completion in OpenAI API.
# for response in model_engine.chat.completions.create(
#     messages=[{"role": "user", "content": f"{prompt}"}],
#     model=MODEL,
#     stream=True,
#     max_tokens=2048, # Amount of max output tokens
#     temperature = 0.0,
# ):
#     for choice in response.choices:
#         print(choice.delta.content, end="", flush=True)
# print("\n")

# # Engine metrics for token per seconds
# metrics = model_engine.metrics()
# token_per_sec = metrics["decode_tokens_per_s"]
# print(f"Token per seconds: {token_per_sec}")