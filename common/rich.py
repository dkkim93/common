import logging
from rich.logging import RichHandler


def get_logger():
    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()]
    )
    logger = logging.getLogger("rich")
    return logger
