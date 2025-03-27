import subprocess
import time

# List of simple commands to execute
commands = [
    'echo Hello, World!',
    'ls',  # List directory contents
    'pwd'  # Print working directory
]

# Loop through the commands and execute them
for command in commands:
    # Run the command using subprocess.Popen
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True
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

    # Sleep for 3 seconds before running the next command
    print("\nSleeping for 3 seconds...\n")
    time.sleep(3)
