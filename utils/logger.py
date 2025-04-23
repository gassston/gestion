import logging
from utils import settings

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s.%(funcName)s] %(message)s",
    datefmt= "%m/%d/%Y %H:%M:%S",
)

def get_logger(name: str = "app"):
    return logging.getLogger(name)
