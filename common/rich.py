import logging
from rich.logging import RichHandler


def get_logger():
    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(
            markup=True,
            rich_tracebacks=True)]
    )
    logger = logging.getLogger("rich")
    return logger
