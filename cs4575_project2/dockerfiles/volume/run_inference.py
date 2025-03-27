import pandas as pd
import os
import time
from prompt import Prompt
from constants import *

def run_inference_on_dataset(dataset_path, inference_method, output_csv):
    df = pd.read_csv(dataset_path)
    responses = []

    for idx, row in df.head(TASKS).iterrows():
        instance = row.to_dict()
        prompt_obj = Prompt(instance)
        prompt_str = prompt_obj.construct_prompt()
        
        start_time = time.time()
        response = inference_method(prompt_str)
        end_time = time.time()
        
        responses.append({
            "instance_id": instance.get("instance_id", ""),
            "prompt": prompt_str,
            "response": response['response'].strip(),
            # "tokens/s": (response['eval_count'] / ((response['eval_duration'] / 1e9)))
            "tokens/s": round(response['eval_count'] / (response['eval_duration'] / 1e9))

        })
        print(f"Generated response for instance: {instance.get('instance_id', '')}")
        
    responses_df = pd.DataFrame(responses)
    responses_df.to_csv(output_csv, index=False)
    print(f"Saved responses to: {output_csv}")