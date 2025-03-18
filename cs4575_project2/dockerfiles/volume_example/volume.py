import os

print(os.listdir())
print(os.listdir('log'))

with open("log/existing_file.txt", "r") as f:
    print(f.read())
with open("log/existing_file2.txt", "r") as f:
    print(f.read())

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='log/example.log',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S')

logger.info('farwegawgrawg')
logger.info('garegaeherash')
logger.info('dshbdftrbwebs')
logger.info('graegaerhaerh')