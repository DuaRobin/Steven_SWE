import logging
from .app_settings import app_settings


def setup_logger(name: str, level: str = app_settings.log_level) -> logging.Logger:
    logger = logging.getLogger(name)
    mapped_level = logging.getLevelNamesMapping().get(level.upper(), logging.INFO)
    logger.setLevel(mapped_level)
    if not logger.hasHandlers():
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(mapped_level)
        default_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        stream_handler.setFormatter(fmt=default_formatter)
        logger.addHandler(hdlr=stream_handler)
    return logger
