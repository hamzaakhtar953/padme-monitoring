import logging
import sys

from uvicorn.logging import DefaultFormatter

FORMAT: str = "%(levelprefix)s [%(asctime)s] - %(message)s"

# Create Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Console Stream Handler
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = DefaultFormatter(FORMAT)

stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)
