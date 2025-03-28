import os
import pandas as pd
from mlc_llm import MLCEngine
from mlc_llm.serve.config import EngineConfig
from prompt import Prompt
from utils import get_next_file_path
from constants import *

# Configuration constants
MODEL = "Qwen2.5-1.5B-Instruct-q4f16_1-MLC"
DATA_PATH = "datasets/SWE-bench_Lite_oracle.csv"
RESULTS_DIR = "results/mlc"

def load_dataset(csv_path: str) -> pd.DataFrame:
    """
    Load the dataset from a CSV file.
    """
    df = pd.read_csv(csv_path)
    return df


def run_experiment(engine: MLCEngine, df: pd.DataFrame, model: str) -> list:
    """
    Iterate through the dataset,
    send each prompt to the engine, print responses and metrics,
    and return a list of token speed metrics.
    """
    experiment_metrics = []

    for index, row in df.head(TASKS).iterrows():
        instance = row.to_dict()
        prompt_obj = Prompt(instance)
        prompt_str = prompt_obj.construct_prompt()

        print(f"Processing question {index}: {prompt_str}\n")

        # Send prompt to the engine (non-streaming)
        response = engine.chat.completions.create(
            messages=[{"role": "user", "content": prompt_str}],
            model=model,
            stream=False,
            max_tokens=2048,
            temperature=0.0,
        )
        response_content = response.choices[0].message.content
        print("Response:")
        print(response_content)
        print("\n")

        # Retrieve engine metrics after processing the prompt.
        metrics = engine.metrics()
        # metrics["decode_tokens_per_s"] = round(metrics["decode_tokens_per_s"])
        token_per_sec = metrics["decode_tokens_per_s"]
        token_per_sec = round(token_per_sec)
        print(f"Token per seconds: {token_per_sec}\n")

        # Save the metric for the current question.
        experiment_metrics.append({
            "instances_id": instance.get("instance_id", ""),
            "prompt": prompt_str,
            "response": response_content,
            "token_per_sec": token_per_sec
        })

    return experiment_metrics


def save_metrics_to_csv(metrics: list, output_file: str) -> None:
    """
    Save token metrics to a CSV file.
    """
    metrics_df = pd.DataFrame(metrics)
    metrics_df.to_csv(output_file, index=False)
    print(f"Metrics saved to {output_file}")


def main():
    # Create engine instance
    engine = MLCEngine(
        model=MODEL,
        device="cuda",
        engine_config=EngineConfig(
            max_single_sequence_length=16384,  # Decrease context window by 50%
            prefill_chunk_size=1024,           # Decrease chunk size by 50%
        )
    )

    # Load dataset from CSV
    df = load_dataset(DATA_PATH)

    # Run the experiment
    token_metrics = run_experiment(engine, df, MODEL)

    # Determine the next available file path
    output_file = get_next_file_path(RESULTS_DIR, 'mlc')

    # Save metrics to CSV
    save_metrics_to_csv(token_metrics, output_file)

    print("Experiment with MLC is done, closing engine now")
    engine.terminate()


if __name__ == "__main__":
    main()
