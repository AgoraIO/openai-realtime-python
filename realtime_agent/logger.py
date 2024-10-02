import logging
from datetime import datetime

import colorlog


def setup_logger(
    name: str,
    log_level: int = logging.INFO,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    use_color: bool = True
) -> logging.Logger:
    """Sets up and returns a logger with color and timestamp support, including milliseconds."""

    # Create or get a logger with the given name
    logger = logging.getLogger(name)

    # Prevent the logger from propagating to the root logger (disable extra output)
    logger.propagate = False
    
    # Clear existing handlers to avoid duplicate messages
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set the log level
    logger.setLevel(log_level)

    # Create console handler
    handler = logging.StreamHandler()

    # Custom formatter for adding milliseconds
    class CustomFormatter(colorlog.ColoredFormatter):
        def formatTime(self, record, datefmt=None):
            record_time = datetime.fromtimestamp(record.created)
            if datefmt:
                return record_time.strftime(datefmt) + f",{int(record.msecs):03d}"
            else:
                return record_time.strftime("%Y-%m-%d %H:%M:%S") + f",{int(record.msecs):03d}"

    # Use custom formatter that includes milliseconds
    if use_color:
        formatter = CustomFormatter(
            "%(log_color)s" + log_format,
            datefmt="%Y-%m-%d %H:%M:%S",  # Milliseconds will be appended manually
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
    else:
        formatter = CustomFormatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")

    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger
