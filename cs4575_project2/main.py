import time
import cs4575_project2.utils as utils
from cs4575_project2.energi_custom import EnergiCustom


# save_directory = './results'
energi = EnergiCustom(measure_gpu=True)
energi.start()
def dummy_task():
    for i in range(3):
        time.sleep(i)
        utils.print_color(f'Sleeping for {i}')

dummy_task()
energi.stop()

