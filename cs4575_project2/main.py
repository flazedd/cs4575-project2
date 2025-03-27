import cs4575_project2.utils as utils
from cs4575_project2.energi_custom import EnergiCustom
import random
import os
#
# save_directory = './results/result_1.csv'
# images = ['mlc', 'ollama', 'vllm']
# energi = EnergiCustom(output=save_directory, measure_gpu=True)
# energi.start()
# # def dummy_task():
# #     for i in range(3):
# #         time.sleep(i)
# #         utils.print_color(f'Sleeping for {i}')
# #
# # dummy_task()
# utils.run_docker_with_gpu(image_name=)
# utils.run_docker_container("pytorch_latest")
# energi.stop()

save_directory = './results'
images = ['mlc', 'ollama', 'vllm']
num_iterations = 5  # Set the number of iterations

for i in range(num_iterations):
    # Shuffle the images randomly in each iteration
    random.shuffle(images)

    for image in images:
        # Create a directory for the image if it doesn't exist
        image_dir = os.path.join(save_directory, image)
        os.makedirs(image_dir, exist_ok=True)

        # Define the save path for the CSV
        save_path = os.path.join(image_dir, f"{image}_{i}.csv")

        energi = EnergiCustom(output=save_path, measure_gpu=True)
        energi.start()

        utils.run_docker_with_gpu(image_name=image)

        energi.stop()