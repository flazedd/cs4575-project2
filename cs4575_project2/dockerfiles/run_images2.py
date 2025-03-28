import os
import subprocess
import time

# Get all Dockerfiles in the current directory
dockerfiles = [f for f in os.listdir() if f.endswith('.Dockerfile')]

# Loop over each Dockerfile
for dockerfile in dockerfiles:
    image_name = os.path.splitext(dockerfile)[0]  # Extracts the filename without extension
    print(f"Running image: {image_name} with GPU support")

    # Start the Docker container process using subprocess.Popen
    process = subprocess.Popen(
        [
            'docker', 'run', '--gpus', 'all',
            '--volume', f"{os.path.abspath(os.path.dirname(__file__))}/volume:/app:rw",
            '--interactive', image_name
        ],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # Read and print stdout and stderr in real-time
    while True:
        # Read stdout line by line
        stdout_line = process.stdout.readline()
        if stdout_line:
            print(stdout_line, end='')  # Print stdout immediately

        # Read stderr line by line (if any)
        stderr_line = process.stderr.readline()
        if stderr_line:
            print(stderr_line, end='')  # Print stderr immediately

        # Break the loop if both stdout and stderr are empty
        if stdout_line == '' and stderr_line == '' and process.poll() is not None:
            break

    # Wait for the process to finish
    process.wait()

    # Sleep for 3 seconds before running the next container
    print("\nSleeping for 3 seconds...\n")
    time.sleep(3)
