import os
import requests
from huggingface_hub import hf_hub_url
from tqdm import tqdm

# Replace with your Hugging Face token
HF_TOKEN = "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"

def download_with_progress(repo_id, filenames, local_dir, token):
    # Create the local directory if it doesn't exist
    os.makedirs(local_dir, exist_ok=True)

    headers = {"Authorization": f"Bearer {token}"}  # Authentication header

    for filename in filenames:
        # Define the local filepath where the file will be saved
        local_filepath = os.path.join(local_dir, filename)

        # Check if the file already exists
        if os.path.exists(local_filepath):
            print(f"{filename} already exists at {local_filepath}, skipping download.")
            continue  # Skip the download if the file already exists

        # Get the direct download URL from Hugging Face model hub
        file_url = hf_hub_url(repo_id=repo_id, filename=filename)

        # Get the total file size (this will be used to show the progress bar)
        response = requests.head(file_url, headers=headers)  # Send a head request with authentication
        response.raise_for_status()  # Ensure the request is successful
        total_size = int(response.headers.get('Content-Length', 0))

        # Start downloading the file while showing the progress bar
        with requests.get(file_url, headers=headers, stream=True) as r:
            r.raise_for_status()  # Raise an error if the request fails

            # Create a progress bar
            with open(local_filepath, 'wb') as f:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Downloading {filename}") as pbar:
                    for chunk in r.iter_content(chunk_size=1024):  # Download in 1 KB chunks
                        f.write(chunk)
                        pbar.update(len(chunk))  # Update progress bar with the chunk size

        print(f"\nDownload complete! {filename} saved at {local_filepath}")

# Usage example
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
filenames = [
    "config.json",
    "generation_config.json",
    "model.safetensors.index.json",
    "pytorch_model.bin.index.json",
    "special_tokens_map.json",
    "tokenizer.json",
    "tokenizer_config.json",
    "tokenizer.model",  # This exists instead of vocab.json/merges.txt
    "model-00001-of-00003.safetensors",
    "model-00002-of-00003.safetensors",
    "model-00003-of-00003.safetensors"
]

local_dir = "./models/mistral"

download_with_progress(repo_id, filenames, local_dir, HF_TOKEN)
