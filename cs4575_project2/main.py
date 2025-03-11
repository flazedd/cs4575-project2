import cs4575_project2.utils as utils
from cs4575_project2.energi_custom import EnergiCustom


save_directory = './results/result_1.csv'
energi = EnergiCustom(output=save_directory, measure_gpu=True)
energi.start()
# def dummy_task():
#     for i in range(3):
#         time.sleep(i)
#         utils.print_color(f'Sleeping for {i}')
#
# dummy_task()
utils.run_docker_container("pytorch_latest")
energi.stop()

