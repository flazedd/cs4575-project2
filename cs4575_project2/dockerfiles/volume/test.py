import os
import torch

def check_gpu():
    if torch.cuda.is_available():
        print(f"GPU is available! CUDA device: {torch.cuda.get_device_name(0)}")
    else:
        print("GPU is not available. Running on CPU.")

def list_files_in_current_directory():
    current_dir = os.getcwd()
    parent_dir = os.path.basename(os.path.dirname(current_dir))

    print(f"Parent Directory: {parent_dir}")
    print(f"Current Working Path: {current_dir}\n")

    for file_name in os.listdir(current_dir):
        file_path = os.path.join(current_dir, file_name)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    line_count = sum(1 for _ in file)
                print(f"{file_name}: {line_count} lines")
            except Exception as e:
                print(f"{file_name}: Could not read file ({e})")


if __name__ == "__main__":
    print('Main...')
    list_files_in_current_directory()
    check_gpu()