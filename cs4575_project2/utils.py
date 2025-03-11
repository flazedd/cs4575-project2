from colorama import Fore, Style
import docker
import os
import sys
from datetime import datetime
import pytz

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
    """Runs a Docker container with the given image name and streams logs in real-time."""

    client = docker.from_env()

    print_color(f"Running {image_name} container...")

    container = client.containers.run(
        image_name,
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





# def check_image_exists(image_name):
#     """Check if the Docker image exists."""
#     client = docker.from_env()
#     try:
#         client.images.get(image_name)
#         return True  # Image already exists
#     except docker.errors.ImageNotFound:
#         return False  # Image doesn't exist
#
# def get_dockerfile_timestamp(dockerfile_path):
#     """Get the last modified time of the Dockerfile."""
#     return os.path.getmtime(dockerfile_path)
#
# def convert_to_local_timezone(timestamp, timezone="Europe/Amsterdam"):
#     """Convert the timestamp to the local timezone."""
#     # If timestamp is in float form (e.g., Unix timestamp), convert it to a datetime object
#     if isinstance(timestamp, float):
#         utc_time = datetime.fromtimestamp(timestamp, tz=pytz.utc)
#     else:
#         # If timestamp is in string form (ISO 8601 format), ensure it's truncated properly
#         if timestamp.endswith('Z'):
#             timestamp = timestamp[:-1]
#
#         # Truncate the timestamp to match the microsecond precision (if nanoseconds are present)
#         timestamp = timestamp[:26]  # Only consider up to microseconds
#         utc_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
#
#     # Set the timezone to UTC
#     utc_time = utc_time.replace(tzinfo=pytz.utc)
#
#     # Convert to local timezone
#     local_time = utc_time.astimezone(pytz.timezone(timezone))
#
#     return local_time
#
# def needs_rebuild(image_name, dockerfile_path, timezone="Europe/Amsterdam"):
#     """Check if the Docker image needs to be rebuilt."""
#     if check_image_exists(image_name):
#         client = docker.from_env()
#         # Get image creation time
#         image = client.images.get(image_name)
#         image_creation_time = image.attrs['Created']
#
#         # Convert image creation time to local timezone
#         image_creation_time_local = convert_to_local_timezone(image_creation_time, timezone)
#
#         # Get Dockerfile modification time and convert to local timezone
#         dockerfile_timestamp = get_dockerfile_timestamp(dockerfile_path)
#         dockerfile_timestamp_local = convert_to_local_timezone(dockerfile_timestamp, timezone)
#
#         # Print both timestamps in human-readable format
#         print(f"Image creation timestamp (local): {image_creation_time_local.strftime('%Y-%m-%d %H:%M:%S')}")
#         print(f"Dockerfile modification timestamp (local): {dockerfile_timestamp_local.strftime('%Y-%m-%d %H:%M:%S')}")
#
#         # Compare timestamps and return result
#         rebuild = dockerfile_timestamp_local > image_creation_time_local
#         print(f"Rebuild needed: {rebuild}")
#         return rebuild
#
#     # If the image doesn't exist, it needs to be built
#     print(f"Image '{image_name}' does not exist. Rebuild needed.")
#     return True
#
# def rebuild_docker_image(image_name, dockerfile_full_path, timezone="Europe/Amsterdam"):
#     """Check if a rebuild is necessary and rebuild the Docker image if needed."""
#     # Extract directory and filename from the full Dockerfile path
#     dockerfile_dir, dockerfile_name = os.path.split(dockerfile_full_path)
#
#     # Check if rebuild is necessary
#     if needs_rebuild(image_name, dockerfile_full_path, timezone):
#         print(f"Rebuilding Docker image: {image_name}...")
#
#         client = docker.from_env()
#
#         if check_image_exists(image_name):
#             print(f"Deleting old image: {image_name}...")
#             try:
#                 client.images.remove(image_name, force=True)
#                 print(f"Old image '{image_name}' deleted successfully.")
#             except docker.errors.ImageNotFound:
#                 print(f"Image '{image_name}' not found for deletion.")
#             except docker.errors.APIError as e:
#                 print(f"Error deleting image: {e}")
#
#         # Now rebuild the image
#         try:
#             # Use the low-level Docker API for building the image with a custom Dockerfile
#             build_logs = client.api.build(
#                 path=dockerfile_dir,
#                 tag=image_name,
#                 dockerfile=dockerfile_name,
#                 rm=True,  # Remove intermediate containers after build
#                 decode=True  # Decode the logs as JSON
#             )
#
#             # Buffer for accumulating partial log lines
#             log_buffer = ""
#
#             # Stream the build logs in real-time
#             for log in build_logs:
#                 if 'stream' in log:
#                     log_str = log['stream']
#                     log_buffer += log_str
#
#                     # Check if we have a complete line
#                     if '\n' in log_buffer:
#                         # Split the buffer into lines and print each line
#                         lines = log_buffer.split('\n')
#                         for line in lines[:-1]:  # Ignore the last part if it's incomplete
#                             print(line.strip())
#                         log_buffer = lines[-1]  # Keep the incomplete part for the next iteration
#
#         except docker.errors.BuildError as e:
#             print(f"Build failed: {e}", file=sys.stderr)
#         except Exception as e:
#             print(f"An error occurred: {e}", file=sys.stderr)
#
#     else:
#         print(f"Image '{image_name}' is up to date. Skipping build.")