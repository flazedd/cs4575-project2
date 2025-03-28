import time
import requests
import ollama
from utils import get_next_file_path  # Importing the generalized function
from run_inference import run_inference_on_dataset
from constants import *

# Configuration
MODEL_NAME = "qwen2.5:0.5b"
# RESULTS_DIR = "results/ollama"
RESULTS_DIR = f"{RESULT_FOLDER}/ollama"
FILE_PREFIX = "ollama"


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
    print(f"Loading model {MODEL_NAME} with Ollama...")
    try:
        ollama.pull(MODEL_NAME)
        print(f"Model {MODEL_NAME} loaded successfully")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False


def ollama_inference(prompt):
    result = ollama.generate(model=MODEL_NAME,
                             prompt=prompt,
                             options={
                                 "temperature": 0,
                                 "max_tokens": 2048
                             })
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


if __name__ == "__main__":
    main()
