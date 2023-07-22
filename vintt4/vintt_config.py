from yaml import safe_load,safe_dump
from loguru import logger
from pydantic import ValidationError

from vintt4.types.vintt_config_types import VinttConfig, VinttTrackItem

def loadVinttConfig(path:str)->VinttConfig:
    """load vintt config from file or return default if failed"""

    try:
        with open(path,"r",encoding="utf8") as file:
            return VinttConfig.parse_obj(safe_load(file))

    except ValidationError:
        logger.error("invalid vintt config")
        raise Exception("validation error")

    except FileNotFoundError:
        logger.error("could not find vintt config: {}",path)
        raise Exception("missing vintt config")

def addCategoryToConfig(path:str,program:str,category:str)->None:
    """write to vintt config, adding a new category"""

    config:VinttConfig=loadVinttConfig(path)

    if program not in config.trackItems:
        logger.error("tried to add category to {}, but was not in config",program)
        return

    item:VinttTrackItem=config.trackItems[program]

    if not item.categories:
        item.categories=[]

    if category in item.categories:
        logger.warning("tried to add category {} to {}, but it was already there",category,program)
        return

    item.categories.append(category)

    with open(path,"w",encoding="utf-8") as wfile:
        safe_dump(config.dict(),wfile,allow_unicode=True)