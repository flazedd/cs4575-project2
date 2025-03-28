from tensorrt_llm import LLM, SamplingParams
import time
from prompt import Prompt
from utils import get_next_file_path
from constants import *
import pandas as pd

# Configuration constants
MODEL = "./TinyLlama-1.1B-Chat-v1.0"
# MODEL = "./Qwen2.5-1.5B-Instruct-AWQ"
DATA_PATH = "datasets/SWE-bench_Lite_oracle.csv"
RESULTS_DIR = "results/tensorrt"

def load_dataset(csv_path: str) -> pd.DataFrame:
    """
    Load the dataset from a CSV file.
    """
    df = pd.read_csv(csv_path)
    return df

def save_metrics_to_csv(metrics: list, output_file: str) -> None:
    """
    Save token metrics to a CSV file.
    """
    metrics_df = pd.DataFrame(metrics)
    metrics_df.to_csv(output_file, index=False)
    print(f"Metrics saved to {output_file}")

def main():
    """
    Run the experiment with {TASKS} amount of prompts with the TensorRT library

    Returns: List of metrics
    """
    sampling_params = SamplingParams(temperature=0, top_p=0.95)

    # Initialize model
    llm = LLM(model=MODEL)
    print("Model loaded successfully\n")

    print("Starting Experiments ...")
    df = load_dataset(DATA_PATH)
    experiment_metrics = []

    for index, row in df.head(TASKS).iterrows():
        instance = row.to_dict()
        prompt_obj = Prompt(instance)
        prompt_str = prompt_obj.construct_prompt()

        print(f"Processing question {index}")

        # Send prompt to the engine
        start_time = time.time()

        # INPUT CAPPED 2048 TOKENS ???
        outputs = llm.generate([prompt_str[:2048]], sampling_params)
        duration = time.time() - start_time

        generated_text = outputs[0].outputs[0].text

        print("Response:")
        print(generated_text)
        print()

        # Compute metrics
        token_count = len(llm.tokenizer.encode(generated_text))
        tokens_per_sec = token_count / duration if duration > 0 else 0

        duration = round(duration)

        # Save the metric for the current question.
        experiment_metrics.append({
            "instance_id": instance.get("instance_id", ""),
            "prompt": prompt_str,
            "response": generated_text,
            "tokens_per_sec": tokens_per_sec,
            "seconds": duration
        })

    return experiment_metrics


if __name__ == '__main__':
    results = main()
    output_file = get_next_file_path(RESULTS_DIR, 'tensorrt')
    save_metrics_to_csv(results, output_file)
