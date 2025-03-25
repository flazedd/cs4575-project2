import os
import json
import time
import pandas as pd
import ollama
import ast
from tqdm import tqdm
import requests

# Configuration
MODEL_NAME = "qwen2.5:0.5b"  
DATASET_PATH = "/app/dataset/mmlu_stem_subset.csv"  
RESULTS_PATH = "/app/results/responses.json"

def wait_for_ollama(max_attempts=10):
    print("Checking if Ollama service is ready...")
    attempt = 0
    while attempt < max_attempts:
        try:
            # Try to ping the Ollama API
            response = requests.get("http://localhost:11434/api/version")
            if response.status_code == 200:
                print("Ollama service is ready!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        
        print(f"Ollama service not ready yet. Attempt {attempt+1}/{max_attempts}")
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

def format_prompt(row):
    question = row['question']
    
    try:
        choices = ast.literal_eval(row['choices'])
    except (ValueError, SyntaxError):
        # Fallback if parsing fails
        choices = row['choices'].strip('[]').split(',')
    
    formatted_choices = ""
    for i, choice in enumerate(choices):
        label = chr(65 + i)  # Convert 0 to 'A', 1 to 'B', etc.
        formatted_choices += f"{label}. {choice}" + "\n"
    
    # Construct the full prompt
    full_prompt = f"""
Question: {question}

Choices:
{formatted_choices}

Please select the best answer from the choices above.
"""
    return full_prompt

# Process a single prompt
def process_prompt(prompt):
    try:
        response = ollama.generate(
            model=MODEL_NAME,
            prompt=prompt,
            options={
                "temperature": 0,  
                "top_p": 0.9,
                "max_tokens": 50
            }
        )
        return response["response"].strip()
    except Exception as e:
        print(f"Error processing prompt: {e}")
        return f"Error: {str(e)}"


def main():
    if not wait_for_ollama():
        print("Cannot proceed without Ollama service")
        return

    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    
    if not load_model():
        print("Failed to load model, cannot proceed")
        return
    
    print(f"Loading dataset from {DATASET_PATH}")
    try:
        df = pd.read_csv(DATASET_PATH)
        print(f"Loaded dataset with {len(df)} rows and columns: {df.columns.tolist()}")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return
    
    required_columns = ['question', 'choices']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: Dataset is missing required columns: {missing_columns}")
        return
    
    with open(RESULTS_PATH, 'w') as f:
        for i, row in tqdm(df.iterrows(), total=len(df)):
            prompt = format_prompt(row)
    
            start_time = time.time()
            response = process_prompt(prompt)
            end_time = time.time()
            
            # Create result object
            result = {
                'prompt_id': i,
                'question': row['question'],
                'choices': row['choices'],
                'response': response,
                'processing_time': end_time - start_time
            }
            f.write(json.dumps(result) + '\n')
            time.sleep(0.1)
    
    print(f"Completed processing. Results saved to {RESULTS_PATH}")

if __name__ == "__main__":
    main()