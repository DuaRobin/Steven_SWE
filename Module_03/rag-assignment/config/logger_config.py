import logging
from pathlib import Path
from .app_settings import app_settings

MODULE_DIR = Path(__file__).resolve().parents[2]


def setup_logger(
    name: str, level: str = app_settings.log_level, log_file: str = ""
) -> logging.Logger:
    logger = logging.getLogger(name=log_file if log_file else name)
    mapped_level = logging.getLevelNamesMapping().get(level.upper(), logging.INFO)
    logger.setLevel(mapped_level)
    default_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    if not logger.hasHandlers():
        if log_file:
            file_handler = logging.FileHandler(
                filename=f"{MODULE_DIR}/logs/{log_file}.log",
                mode="w",
                encoding="utf-8",
            )
            file_handler.setLevel(mapped_level)
            file_handler.setFormatter(fmt=default_formatter)
            logger.addHandler(hdlr=file_handler)
        else:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(mapped_level)
            stream_handler.setFormatter(fmt=default_formatter)
            logger.addHandler(hdlr=stream_handler)
    return logger
