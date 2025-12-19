import logging
from datetime import datetime

def setup_logger():
    logger = logging.getLogger("aws-inventory")
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    ch.setFormatter(ch_formatter)
    logger.addHandler(ch)

    fh = logging.FileHandler("aws_inventory.log")
    fh.setLevel(logging.INFO)
    fh_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)

    return logger

logger = setup_logger()

def get_session():
    import boto3
    return boto3.session.Session()

def remove_tz(dt):
    """Convert timezone-aware datetime to naive datetime for Excel."""
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt
