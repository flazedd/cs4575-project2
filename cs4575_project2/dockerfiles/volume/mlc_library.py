import os
import time

import pandas as pd
from mlc_llm import MLCEngine
from mlc_llm.serve.config import EngineConfig
from prompt import Prompt
from utils import get_next_file_path
from constants import *
import subprocess

# Configuration constants
MODEL = "Qwen2.5-Coder-3B-Instruct-q4f16_1-MLC"
MODEL_ENGINE = f"{MODEL}-cuda.so"
DATA_PATH = "datasets/SWE-bench_Lite_oracle.csv"
RESULTS_DIR = f"{RESULT_FOLDER}/mlc"

def compile_model():
    cmd = [
        "mlc_llm",
        "compile",
        MODEL,
        "--device", "cuda",
        "-o", f"{MODEL}/{MODEL_ENGINE}"
    ]
    try:
        result = subprocess.run(cmd, check=True)
        print("Compilation succeeded!")
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Compilation failed!")
        print("Error:", e.stderr)

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
        start_time = time.time()
        print(f"Processing question {index}: {prompt_str}\n")

        # Send prompt to the engine (non-streaming)
        response = engine.chat.completions.create(
            messages=[{"role": "user", "content": prompt_str}],
            model=model,
            stream=False,
            max_tokens=MAX_OUTPUT_TOKENS,
            temperature=TEMPERATURE,
            seed = SEED
        )
        response_content = response.choices[0].message.content
        print("Response:")
        print(response_content)
        print("\n")
        end_time = time.time()

        # Retrieve engine metrics after processing the prompt.
        metrics = engine.metrics()
        # metrics["decode_tokens_per_s"] = round(metrics["decode_tokens_per_s"])
        token_per_sec = metrics["decode_tokens_per_s"]
        token_per_sec = round(token_per_sec)
        print(f"Token per seconds: {token_per_sec}\n")

        elapsed_time_seconds = round(end_time - start_time)

        # Save the metric for the current question.
        experiment_metrics.append({
            "instance_id": instance.get("instance_id", ""),
            "prompt": prompt_str,
            "response": response_content,
            "tokens_per_sec": token_per_sec,
            "seconds": elapsed_time_seconds,
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
    # Compile .so (engine for MLC) if not yet existing
    if not os.path.exists(f"{MODEL}/{MODEL_ENGINE}"):
        print("LOWER prefill_chunk_size (default 8192) inside mlc-chat-config.json or it will not fit on GPU memory")
        compile_model()
        
    # Create engine instance
    engine = MLCEngine(
        model=MODEL,
        model_lib=f"{MODEL}/{MODEL_ENGINE}",
        device="cuda",
        mode="interactive",
        engine_config=EngineConfig(
            max_single_sequence_length=MAX_CONTEXT_WINDOW,
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
    exit(0)


if __name__ == "__main__":
    main()
