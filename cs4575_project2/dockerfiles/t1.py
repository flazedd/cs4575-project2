import os
from huggingface_hub import hf_hub_download, snapshot_download
from llama_cpp import Llama

# Model details
MODEL_REPO = "TheBloke/Mistral-7B-v0.1-GGUF"
MODEL_FILE = "mistral-7b-v0.1.Q4_K_M.gguf"  # Adjust if using a different quantization
LOCAL_MODEL_DIR = "./models"
LOCAL_MODEL_PATH = os.path.join(LOCAL_MODEL_DIR, MODEL_FILE)

# Ensure model directory exists
os.makedirs(LOCAL_MODEL_DIR, exist_ok=True)

# Check if model is already downloaded
if not os.path.exists(LOCAL_MODEL_PATH):
    print("Model not found locally. Downloading...")
    hf_hub_download(repo_id=MODEL_REPO, filename=MODEL_FILE, local_dir=LOCAL_MODEL_DIR)
    # snapshot_download(repo_id=MODEL_REPO, local_dir=LOCAL_MODEL_DIR)

    print("Download complete.")
else:
    print("Model already present. Skipping download.")

# Load the model
print("Loading model...")
llm = Llama(model_path=LOCAL_MODEL_PATH, n_ctx=4096)  # Increase context if needed

# Ask a simple question
question = "What is the capital of France?"
print(f"Question: {question}")

# Generate response
response = llm(question)
print("Response:", response["choices"][0]["text"].strip())
