import logging
import sys

from setting import LOG_LEVEL


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger
