import sys
import time

import cs4575_project2.utils as utils
from cs4575_project2.energi_custom import EnergiCustom
import random
import os

save_directory = './results'
images = ['mlc', 'ollama', 'vllm']


utils.sync_common_files("./dockerfiles/volume/results", "./results", images=images)


num_iterations = 5  # Total number of iterations
first_iteration = 0
last_iteration = num_iterations - 1

def count_files_in_folder(folder):
    """Counts the number of files in a given folder."""
    return sum(len(files) for _, _, files in os.walk(folder))


image_counts = {img: count_files_in_folder(os.path.join(save_directory, img)) for img in images}
min_count = min(image_counts.values())
lowest_count_images = [img for img, count in image_counts.items() if count == min_count]

# Run the first iteration explicitly
for i in [first_iteration] + list(range(1, last_iteration)) + [last_iteration]:
    if i == first_iteration:
        process_order = lowest_count_images  # First iteration: prioritize least-populated folders
        utils.print_color(f'Unfinished work detected, first working on {process_order} to restore balance')
    else:
        random.shuffle(images)  # Shuffle for randomne
        # ss after the first iteration
        process_order = images

    for image in process_order:
        utils.print_color(f'Working on iteration {i} and image {image}')
        # Create a directory for the image if it doesn't exist
        image_dir = os.path.join(save_directory, image)
        os.makedirs(image_dir, exist_ok=True)

        # Define the save path for the CSV
        save_path = os.path.join(image_dir, f"{image}_{i}.csv")

        energi = EnergiCustom(output=save_path, measure_gpu=True)
        energi.start()

        utils.run_docker_with_gpu(image_name=image)

        energi.stop()
        time.sleep(60)