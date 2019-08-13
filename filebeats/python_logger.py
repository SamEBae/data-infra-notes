import logging
import time

logger = logging.getLogger('simple_example')
logger.setLevel(logging.INFO)

# create file handler which logs even debug messages
fh = logging.FileHandler('gg.log')
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

# 'application' code
# logger.debug('debug message')
logger.info('info message')
counter = 0

while True:
	logger.info('info message')
	time.sleep(0.01)

	counter += 1

	if counter == 100000:
		break