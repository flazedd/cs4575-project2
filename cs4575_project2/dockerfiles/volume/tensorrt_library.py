from tensorrt_llm import LLM, SamplingParams, build, Mapping
from tensorrt_llm.llmapi import QuantConfig, QuantAlgo, BuildConfig
from tensorrt_llm.plugin import PluginConfig
from tensorrt_llm.models import QWenForCausalLM
import time
from prompt import Prompt
from utils import get_next_file_path
from constants import *
import pandas as pd
import subprocess
import os
import shutil

# Configuration constants
# MODEL = "./TinyLlama-1.1B-Chat-v1.0"
MODEL = "Qwen2.5-Coder-3B-Instruct-AWQ"
MODEL_TRT = f"{MODEL}-TensorRT"
DATA_PATH = "datasets/SWE-bench_Lite_oracle.csv"
RESULTS_DIR = f"{RESULT_FOLDER}/tensorrt"

def run_command(command, step_name):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(f"{step_name} successful:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"{step_name} failed:")
        print(e.stderr)
        raise

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
    # Initialize model
    sampling_params = SamplingParams(temperature=TEMPERATURE, max_tokens=MAX_OUTPUT_TOKENS, repetition_penalty=REPETITION_PENALTY, top_p=TOP_P, top_k=TOP_K, seed=SEED)
    
    if not os.path.exists(MODEL_TRT):
        # Convert the checkpoint
        convert_command = [
            "python", "convert_checkpoint.py",
            "--model_dir", MODEL,
            "--output_dir", MODEL_TRT
        ]
        run_command(convert_command, "Checkpoint conversion")
    
        # List of files to copy for engine
        files_to_copy = ["tokenizer_config.json", "tokenizer.json", "vocab.json", "generation_config.json"]
        for file in files_to_copy:
            src_path = os.path.join(MODEL, file)
            dst_path = os.path.join(MODEL_TRT, file)
            if os.path.exists(src_path):
                shutil.copy(src_path, dst_path)
                print(f"Copied {src_path} to {dst_path}")
            else:
                print(f"File {src_path} does not exist.")
        
    # Build model engine
    build_config = BuildConfig(max_input_len=MAX_CONTEXT_WINDOW, max_seq_len=MAX_CONTEXT_WINDOW, max_num_tokens=MAX_CONTEXT_WINDOW, max_batch_size=1)
    llm = LLM(model=MODEL_TRT, build_config=build_config)
    if not os.path.exists(os.path.join(MODEL_TRT, "rank0.engine")):
        llm.save(MODEL_TRT) # save engine to folder
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
        outputs = llm.generate([prompt_str], sampling_params)
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
    exit(0)