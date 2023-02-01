import logging
from malcheck_client.config import LOG_PATH

logger = logging.getLogger()
logFormatter = logging.Formatter('%(asctime)s - Malcheck-Client - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fileHandler = logging.FileHandler(LOG_PATH)
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
