from colorama import Fore, Style
import docker
import os
import sys
from datetime import datetime
import pytz
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


import os
import subprocess

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




import subprocess

def remove_all_docker_containers():
    """
    List all Docker containers (including stopped ones) and remove each of them.
    """
    print('Removing all docker containers')
    try:
        # Get the container IDs for all containers (including stopped ones)
        result = subprocess.run(
            ['docker', 'ps', '-a', '-q'],
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

