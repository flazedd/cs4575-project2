from colorama import Fore, Style
import docker
import os
from datetime import datetime
import subprocess

def create_framework_dirs(frameworks, base_dir="./results"):
    """
    Creates directories for each framework inside the specified base directory if they don't already exist.

    Parameters:
    - frameworks (list): A list of framework names.
    - base_dir (str): The base directory where framework folders will be created. Default is "./results".
    """
    os.makedirs(base_dir, exist_ok=True)  # Ensure the base directory exists

    for framework in frameworks:
        framework_dir = os.path.join(base_dir, framework)
        os.makedirs(framework_dir, exist_ok=True)  # Create directory if it doesn't exist
        print(f"Directory created (or already exists): {framework_dir}")


def print_color(message, success=True):
    timestamp = datetime.now().strftime("[%H:%M]")  # Get current time in [HH:MM] format
    prefix = f"{Fore.GREEN}[+]{Style.RESET_ALL}" if success else f"{Fore.RED}[-]{Style.RESET_ALL}"
    print(f"{timestamp} {prefix} {message}")


def run_docker_container(image_name):
    """Runs a Docker container with GPU support and volume mapping."""
    client = docker.from_env()
    volume_path = os.path.join(os.getcwd(), 'dockerfiles', 'volume')

    if os.path.exists(volume_path):
        print(f"The directory exists: {volume_path}")
    else:
        print(f"The directory does not exist: {volume_path}")

    print(f'{volume_path}')

    # k = input(f'enter y/n: ')

    print(f"Running {image_name} with {volume_path} path with GPU support and volume mapping...")

    container = client.containers.run(
        image_name,
        runtime="nvidia",  # Enables GPU support
        volumes={volume_path: {'bind': '/app', 'mode': 'rw'}},
        remove=True,
        stdout=True,
        stderr=True,
        tty=True,
        stdin_open=True,
        detach=True,
    )

    log_buffer = ""  # To accumulate characters until a complete line is received

    for log in container.logs(stream=True, stdout=True, stderr=True):
        log_str = log.decode("utf-8")
        log_buffer += log_str

        # Check if we have a complete line
        if '\n' in log_buffer:
            # Split the buffer into lines and print each line
            lines = log_buffer.split('\n')
            for line in lines[:-1]:  # Ignore the last part if it's incomplete
                print_color(line.strip())
            log_buffer = lines[-1]  # Keep the incomplete part for the next iteration


def run_docker_ps1(image_name):
    """Runs a Docker container with GPU support and volume mapping, executing the PowerShell command."""

    # Get the path to the volume folder
    volume_path = os.path.join(os.getcwd(), 'dockerfiles', 'volume')

    if os.path.exists(volume_path):
        print(f"The directory exists: {volume_path}")
    else:
        print(f"The directory does not exist: {volume_path}")
        return

    print(f"Running {image_name} with GPU support...")

    # Prepare the PowerShell command
    ps_command = f'docker run --gpus all --volume {volume_path}:/app:rw --interactive {image_name}'

    try:
        # Run the PowerShell command via subprocess and capture the output
        result = subprocess.run(ps_command, shell=True, check=True, capture_output=True, text=True)

        # Print the standard output and standard error (if any)
        print("Output:\n", result.stdout)
        if result.stderr:
            print("Error:\n", result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stdout:
            print("Output:\n", e.stdout)
        if e.stderr:
            print("Error:\n", e.stderr)

    print(f"Successfully ran {image_name} with GPU support and volume mapping.")


def run_docker_with_gpu(image_name: str) -> None:
    """
    Run a Docker container with GPU support, mounting the 'dockerfiles/volume' directory as a volume.
    After running the container, it will remove the container.

    :param image_name: The name of the Docker image to run.
    """
    print(f"Running image: {image_name} with GPU support")

    # Define the new path to the volume (dockerfiles/volume)
    volume_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'dockerfiles', 'volume'))

    # Run the container interactively to display its output and capture the container ID
    # result = subprocess.run(
    #     ['docker', 'run', '--gpus', 'all',
    #      '--volume', f"{volume_path}:/app:rw",
    #      '--interactive', '--detach', image_name],
    #     capture_output=True, text=True
    # )

    subprocess.run([
        'docker', 'run', '--gpus', 'all',
        '--volume', f"{volume_path}:/app:rw",
        '--interactive', image_name
    ])

    remove_all_docker_containers()


def remove_all_docker_containers():
    """
    List all Docker containers (including stopped ones) and remove each of them.
    """
    print('Removing all docker containers')
    try:
        # Get the container IDs for all containers (including stopped ones)
        result = subprocess.run(
            ['docker', 'ps', '-q'],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            # Get container IDs from the output
            container_ids = result.stdout.strip().splitlines()

            if container_ids:
                print(f"Found {len(container_ids)} containers. Removing them...")

                # Loop through each container ID and remove it
                for container_id in container_ids:
                    subprocess.run(['docker', 'rm', '-f', container_id])
                    print(f"Removed container {container_id}")
            else:
                print("No containers found to remove.")
        else:
            print(f"Error listing Docker containers: {result.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")


def sync_common_files(project_results, local_results, images):
    """
    Synchronizes specific subdirectories, keeping only files that exist in both locations.

    Args:
        project_results (str): Path to the first results directory (e.g., project folder).
        local_results (str): Path to the second results directory (e.g., local folder).
        images (list): List of subdirectories inside results to consider.
    """
    def get_files_by_folder(root, subdirs):
        """Returns a dictionary with folder paths as keys and sets of filenames as values."""
        files_dict = {}
        for subdir in subdirs:
            full_subdir_path = os.path.join(root, subdir)
            if not os.path.exists(full_subdir_path):
                continue  # Skip if the subdirectory doesn't exist
            for dirpath, _, filenames in os.walk(full_subdir_path):
                relative_path = os.path.relpath(dirpath, root)  # Get relative path from root
                files_dict[relative_path] = set(filenames)  # Store filenames in a set
        return files_dict

    # Get file lists for both directories
    project_files = get_files_by_folder(project_results, images)
    local_files = get_files_by_folder(local_results, images)

    # Find common subdirectories
    common_folders = set(project_files.keys()) & set(local_files.keys())

    # Process each common folder
    for folder in common_folders:
        project_folder_path = os.path.join(project_results, folder)
        local_folder_path = os.path.join(local_results, folder)

        # Get common files in the current folder
        common_files = project_files[folder] & local_files[folder]

        # Remove files that are not in both locations
        for file in project_files[folder] - common_files:
            file_path = os.path.join(project_folder_path, file)
            print_color(f"Removing from project: {file_path}")
            os.remove(file_path)

        for file in local_files[folder] - common_files:
            file_path = os.path.join(local_folder_path, file)
            print_color(f"Removing from local: {file_path}")
            os.remove(file_path)

    print_color("Synchronization complete. Only common files are kept.")


def count_files_in_folder(folder):
    """Counts the number of files in a given folder."""
    return sum(len(files) for _, _, files in os.walk(folder))


def get_next_csv_number(image_dir):
    """Finds the highest iteration number for CSV files in a given directory and returns the next one."""
    existing_files = [f for f in os.listdir(image_dir) if f.endswith('.csv')]
    if not existing_files:
        return 0  # If no CSVs exist, start from 0

    # Get the maximum index number from the filenames
    max_index = max(int(f.split('_')[1].split('.')[0]) for f in existing_files)
    return max_index + 1


def ensure_directories_exist(save_directory, llm_path, images):
    """
    Ensure that the directories for each image under save_directory and llm_path exist.
    If they do not exist, the function will create them.

    :param save_directory: The base directory for saving images.
    :param llm_path: The base path for the LLM-related images.
    :param images: A list of image names for which directories need to be created.
    """
    print_color('Ensuring directories exist...')
    for image in images:
        # Define full paths for both directories
        save_image_path = os.path.join(save_directory, image)
        llm_image_path = os.path.join(llm_path, image)

        # Check if the save_image_path exists, if not, create it
        if not os.path.exists(save_image_path):
            os.makedirs(save_image_path)
            print(f"Created directory: {save_image_path}")
        else:
            print(f"Directory already exists: {save_image_path}")

        # Check if the llm_image_path exists, if not, create it
        if not os.path.exists(llm_image_path):
            os.makedirs(llm_image_path)
            print(f"Created directory: {llm_image_path}")
        else:
            print(f"Directory already exists: {llm_image_path}")



# Example usage:
# save_directory = 'results'
# images = ['mlc', 'ollama', 'vllm']
# ensure_directories_exist(save_directory, images)
