from yaml import safe_load
from loguru import logger
from pydantic import ValidationError

from vintt4.types.vintt_config_types import VinttConfig

def loadVinttConfig(path:str)->VinttConfig:
    """load vintt config from file or return default if failed"""

    try:
        with open(path,"r",encoding="utf8") as file:
            return VinttConfig.parse_obj(safe_load(file))

    except ValidationError:
        logger.error("invalid vintt config, exiting")
        raise Exception("validation error")

    except FileNotFoundError:
        logger.error("could not find vintt config: {}",path)
        raise Exception("missing vintt config")