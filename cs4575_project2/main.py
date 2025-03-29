import time
import cs4575_project2.utils as utils
from cs4575_project2.energi_custom import EnergiCustom
import random
import os
from cs4575_project2.dockerfiles.volume.constants import RESULT_FOLDER
save_directory = RESULT_FOLDER

images = ['mlc', 'ollama', 'vllm']
llm_path = f"./dockerfiles/volume/{save_directory}"

utils.ensure_directories_exist(save_directory, llm_path, images)
utils.sync_common_files(llm_path, save_directory, images=images)


num_iterations = 10
image_counts = {img: utils.count_files_in_folder(os.path.join(save_directory, img)) for img in images}
min_count = min(image_counts.values())
lowest_count_images = [img for img, count in image_counts.items() if count == min_count]

# Run the first iteration explicitly
for i in range(num_iterations):
    if i == 0:
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
        # save_path = os.path.join(image_dir, f"{image}_{i}.csv")
        next_csv_number = utils.get_next_csv_number(image_dir)
        save_path = os.path.join(image_dir, f"{image}_{next_csv_number}.csv")

        energi = EnergiCustom(output=save_path, measure_gpu=True)
        energi.start()

        utils.run_docker_with_gpu(image_name=image)

        energi.stop()
        time.sleep(60)