import logging
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'app.log')

def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
    return logger
