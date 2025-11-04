import logging
logger = logging.getLogger(__name__)

def division(a, b):
    result = float(b) / float(a)
    logger.info(f"Dividing {b} / {a} = {result}")
    return float(b) / float(a)
