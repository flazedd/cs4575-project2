import time
import pandas as pd
from vllm import LLM
from prompt import Prompt  # Reuse the same Prompt class
from utils import get_next_file_path  # Import the generalized function
from constants import *

# Configuration constants
MODEL = "Qwen2.5-Coder-14B-Instruct-AWQ"
DATA_PATH = DATASET_PATH
RESULTS_DIR = f"{RESULT_FOLDER}/vllm"
FILE_PREFIX = "vllm"


def load_dataset(csv_path: str) -> pd.DataFrame:
    """Load the dataset from a CSV file."""
    return pd.read_csv(csv_path)


def run_experiment(llm: LLM, df: pd.DataFrame, sampling_params: dict) -> list:
    """Run inference experiment and collect performance metrics."""
    experiment_metrics = []
    # for index, row in df.iterrows():
    for index, row in df.head(TASKS).iterrows():
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
        # tokens_per_sec = generated_tokens / time_taken
        tokens_per_sec = round(generated_tokens / time_taken)
        time_taken = round(time_taken)

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
            "tokens_per_sec": tokens_per_sec,
            "seconds": time_taken,
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
        max_model_len=MAX_CONTEXT_WINDOW,  # Equivalent to MLC's max_single_sequence_length
    )

    # Configure sampling parameters
    sampling_params = llm.get_default_sampling_params()
    sampling_params.temperature = TEMPERATURE
    sampling_params.max_tokens = MAX_OUTPUT_TOKENS
    sampling_params.seed = SEED
    sampling_params.repetition_penalty = REPETITION_PENALTY
    sampling_params.top_k = TOP_K
    sampling_params.top_p = TOP_P

    # Load dataset
    df = load_dataset(DATA_PATH)

    # Run experiment
    token_metrics = run_experiment(llm, df, sampling_params)

    # Save results
    save_metrics_to_csv(token_metrics, output_csv)

    print("Experiment with vLLM is done!")
    del llm
    exit(0)


if __name__ == "__main__":
    main()
