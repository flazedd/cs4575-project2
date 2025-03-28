import os
import subprocess

# Get all Dockerfiles in the current directory
dockerfiles = [f for f in os.listdir() if f.endswith('.Dockerfile')]

# Loop over each Dockerfile
for dockerfile in dockerfiles:
    image_name = os.path.splitext(dockerfile)[0]  # Extracts the filename without extension
    print(f"Running image: {image_name} with GPU support")

    # Run the container interactively to display its output
    subprocess.run([
        'docker', 'run', '--gpus', 'all',
        '--volume', f"{os.path.abspath(os.path.dirname(__file__))}/volume:/app:rw",
        '--interactive', image_name
    ])
