from loguru import logger
from loguru._defaults import LOGURU_FORMAT
from sys import stdout

# --- config ---
USE_MINIMAL_FORMAT:bool=False
USE_MINIMAL_FORMAT2:bool=True
# --- end config ---

LOG_FORMAT:str=LOGURU_FORMAT
if USE_MINIMAL_FORMAT:
    LOG_FORMAT=(
        "<green>{time:HH:mm:ss}</green> | "+
        "<level>{level: <8}</level> | "+
        "<level>{message}</level>"
    )

if USE_MINIMAL_FORMAT2:
    LOG_FORMAT="<level>{message}</level>"

logger.remove()
logger.add(
    stdout,
    level="INFO",
    format=LOG_FORMAT
)