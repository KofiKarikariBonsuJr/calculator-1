import logging
logger = logging.getLogger(__name__)

def subtraction(a, b):
    a = float(a)
    b = float(b)
    c = b - a
    logger.info(f"Subtracting {a} from {b} = {c}")
    return c