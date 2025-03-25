import pandas as pd
import os
from ..scripts.prompt import Prompt

def run_inference_on_dataset(dataset_path, inference_method, output_csv):
    df = pd.read_csv(dataset_path)
    responses = []

    for idx, row in df.head(5).iterrows():
        instance = row.to_dict()
        prompt_obj = Prompt(instance)
        prompt_str = prompt_obj.construct_prompt()
        response = inference_method(prompt_str)
        
        responses.append({
            "instance_id": instance.get("instance_id", ""),
            # "prompt": prompt_str,
            # "response": response['response'].strip(),
            "tokens/s": (response['eval_count'] / (response['eval_duration'] / 1e9))
        })
        print(f"Generated response for instance: {instance.get("instance_id", "")}")
        
    responses_df = pd.DataFrame(responses)
    responses_df.to_csv(output_csv, index=False)
    print(f"Saved responses to: {output_csv}")
