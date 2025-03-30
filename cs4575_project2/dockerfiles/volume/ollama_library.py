import time
import requests
import ollama
from utils import get_next_file_path  # Importing the generalized function
from run_inference import run_inference_on_dataset
from constants import *
import os
import subprocess

# Configuration
MODEL_NAME = "Qwen2.5-Coder-3B-Instruct-Q4_K_L"
# RESULTS_DIR = "results/ollama"
RESULTS_DIR = f"{RESULT_FOLDER}/ollama"
FILE_PREFIX = "ollama"
parameters = {
    "num_ctx": MAX_CONTEXT_WINDOW,
    "temperature": TEMPERATURE,
    "num_predict": MAX_OUTPUT_TOKENS,
    "repeat_penalty": REPETITION_PENALTY,
    "top_k": TOP_K,
    "top_p": TOP_P,
    "seed": SEED
}


def wait_for_ollama(max_attempts=10):
    print("Checking if Ollama service is ready...")
    attempt = 0
    while attempt < max_attempts:
        try:
            response = requests.get("http://localhost:11434/api/version")
            if response.status_code == 200:
                print("Ollama service is ready!")
                return True
        except requests.exceptions.ConnectionError:
            pass

        print(f"Ollama service not ready yet. Attempt {attempt + 1}/{max_attempts}")
        time.sleep(5)
        attempt += 1

    print("Failed to connect to Ollama service after multiple attempts")
    return False

def load_model():
    print(f"Creating model {MODEL_NAME} using subprocess...")
    try:
        # Construct the absolute path for the GGUF file
        gguf_path = os.path.abspath(f"{MODEL_NAME}.gguf")
        if not os.path.exists(gguf_path):
            raise FileNotFoundError(f"GGUF file not found at {gguf_path}")

        # The Modelfile in the current directory will be used.
        cmd = ["ollama", "create", MODEL_NAME]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error creating model:", result.stderr)
            return False
        print("Model created successfully:", result.stdout)
        return True
    except Exception as e:
        print("Error creating model using subprocess:", e)
        return False

def ollama_inference(prompt):
    result = ollama.generate(model=MODEL_NAME,
                             prompt=prompt,
                             options=parameters)
    return result

def main():
    dataset_path = "datasets/SWE-bench_Lite_oracle.csv"

    # Determine the next available file path
    output_csv = get_next_file_path(RESULTS_DIR, FILE_PREFIX)

    if not wait_for_ollama():
        print("Cannot proceed without Ollama service")
        return

    if not load_model():
        print("Failed to load model, cannot proceed")
        return

    try:
        run_inference_on_dataset(
            dataset_path=dataset_path,
            inference_method=ollama_inference,
            output_csv=output_csv
        )
        print(f"Results saved to {output_csv}")
    except Exception as e:
        print(f"Error: {e}")
    exit(0)


if __name__ == "__main__":
    main()
