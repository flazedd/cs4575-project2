import docker
import os


def build_and_run_docker():
    # Initialize Docker client
    client = docker.from_env()

    try:
        # Step 1: Build the Docker image from the Dockerfile in the current directory
        print("Building Docker image...")
        image, logs = client.images.build(path=".", dockerfile="Dockerfile", tag="pytorch-ml")


        # Output the logs from the build process
        for log in logs:
            print(log.get('stream', '').strip())

        # Step 2: Run the container from the built image and execute the workload
        print("Running container with PyTorch workload...")
        container = client.containers.run("pytorch-ml", detach=True)

        # Step 3: Print the logs (training progress)
        for log in container.logs(stream=True, follow=True):
            print(log.decode("utf-8"), end='')

        # Step 4: Wait for the container to finish
        container.wait()

        print("Training finished!")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Cleanup by removing the container
        try:
            container.remove()
        except:
            pass


if __name__ == "__main__":
    build_and_run_docker()
