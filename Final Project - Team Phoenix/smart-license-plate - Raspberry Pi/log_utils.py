# --- log_utils.py ---
import logging
import os

LOG_PATH = "logs/detection.log"
os.makedirs('logs', exist_ok=True)

def get_logger():
    logger = logging.getLogger("DetectionLogger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        fh = logging.FileHandler(LOG_PATH)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
