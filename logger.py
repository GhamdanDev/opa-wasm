import logging

def setup_logger():
    """Configure and return the application logger"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger

logger = setup_logger()
