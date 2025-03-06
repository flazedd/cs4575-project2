import docker
import os

# Initialize Docker client
client = docker.from_env()

# Define image name
image_name = "pytorch_training"

# Get the absolute path to the directory containing Dockerfile
dockerfile_path = os.path.abspath(".")

# Build the Docker image
print(f"Building Docker image: {image_name}...")
image, logs = client.images.build(path=dockerfile_path, tag=image_name)

# Print build logs
for log in logs:
    if "stream" in log:
        print(log["stream"].strip())

# Run the container
print(f"Running {image_name} container...")

container = client.containers.run(
    image_name,
    remove=True,
    stdout=True,
    stderr=True
)

# Print container logs (training output)
print("Container Output:\n", container.decode())
