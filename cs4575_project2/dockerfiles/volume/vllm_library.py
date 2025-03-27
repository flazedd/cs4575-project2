import time
import pandas as pd
from vllm import LLM
from prompt import Prompt  # Reuse the same Prompt class
from utils import get_next_file_path  # Import the generalized function

# Configuration constants
MODEL = "Qwen2.5-1.5B-Instruct-AWQ"
DATA_PATH = "datasets/SWE-bench_Lite_oracle.csv"
RESULTS_DIR = "results/vllm"
FILE_PREFIX = "vllm"


def load_dataset(csv_path: str) -> pd.DataFrame:
    """Load the dataset from a CSV file."""
    return pd.read_csv(csv_path)


def run_experiment(llm: LLM, df: pd.DataFrame, sampling_params: dict) -> list:
    """Run inference experiment and collect performance metrics."""
    experiment_metrics = []
    # for index, row in df.iterrows():
    for index, row in df.head(10).iterrows():
        instance = row.to_dict()
        prompt_obj = Prompt(instance)
        prompt_str = prompt_obj.construct_prompt()

        print(f"Processing instance {index}: {prompt_str}\n")

        # Time the generation call
        start_time = time.time()
        outputs = llm.generate(prompt_str, sampling_params)
        end_time = time.time()

        # Calculate performance metrics
        time_taken = end_time - start_time
        generated_tokens = len(outputs[0].outputs[0].token_ids)
        tokens_per_sec = generated_tokens / time_taken

        # Extract response text
        response_text = outputs[0].outputs[0].text
        print("Response:")
        print(response_text)
        print(f"\nTokens per second: {tokens_per_sec:.2f}\n")

        # Store results
        experiment_metrics.append({
            "instance_id": instance.get("instance_id", ""),
            "prompt": prompt_str,
            "response": response_text,
            "token_per_sec": tokens_per_sec
        })

    return experiment_metrics


def save_metrics_to_csv(metrics: list, output_file: str) -> None:
    """Save metrics to CSV file."""
    metrics_df = pd.DataFrame(metrics)
    metrics_df.to_csv(output_file, index=False)
    print(f"Metrics saved to {output_file}")


def main():
    # Get the next available file path using the generalized function
    output_csv = get_next_file_path(RESULTS_DIR, FILE_PREFIX)

    # Initialize vLLM engine with equivalent config
    llm = LLM(
        model=MODEL,
        device="cuda",
        quantization="awq",
        max_model_len=16384,  # Equivalent to MLC's max_single_sequence_length
    )

    # Configure sampling parameters
    sampling_params = llm.get_default_sampling_params()
    sampling_params.temperature = 0.0
    sampling_params.max_tokens = 2048

    # Load dataset
    df = load_dataset(DATA_PATH)

    # Run experiment
    token_metrics = run_experiment(llm, df, sampling_params)

    # Save results
    save_metrics_to_csv(token_metrics, output_csv)

    print("Experiment with vLLM is done!")


if __name__ == "__main__":
    main()
