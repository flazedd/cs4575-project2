# utils.py
import os


def get_next_file_path(results_dir: str, file_prefix: str, file_extension: str = ".csv") -> str:
    """
    Get the next available file path for saving results in the format {prefix}_{i}{extension}.

    :param results_dir: The directory to check for existing files.
    :param file_prefix: The prefix for the files (e.g., 'ollama').
    :param file_extension: The file extension (default is ".csv").
    :return: The path to the next available file.
    """
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        return os.path.join(results_dir, f"{file_prefix}_0{file_extension}")

    existing_files = [f for f in os.listdir(results_dir) if f.startswith(file_prefix) and f.endswith(file_extension)]
    if not existing_files:
        return os.path.join(results_dir, f"{file_prefix}_0{file_extension}")

    # Extract numbers from existing filenames
    file_numbers = []
    for file in existing_files:
        try:
            number = int(file.split("_")[1].split(".")[0])
            file_numbers.append(number)
        except ValueError:
            continue

    # Get the next available file number
    next_file_number = max(file_numbers, default=-1) + 1
    return os.path.join(results_dir, f"{file_prefix}_{next_file_number}{file_extension}")
