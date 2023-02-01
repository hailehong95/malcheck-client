import logging
from malcheck_client.config import LOG_PATH

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - Malcheck-Client - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
