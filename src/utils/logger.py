import logging
from src.config.settings import settings

def setup_logger() -> logging.Logger:
    logger = logging.getLogger("sql_ai_assistant")

    if logger.hasHandlers():
        return logger

    logger.setLevel(settings.log_level.upper())

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.propagate = False

    return logger

logger = setup_logger()
