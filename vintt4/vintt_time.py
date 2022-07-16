from yaml import safe_load,safe_dump
from loguru import logger

from vintt4.types.vintt_time_types import VinttTimeFile

def incrementTime(
    process:str,
    category:str,
    time:int,
    path:str
)->None:
    """increment a process's time in a category. writes to the time file"""

    timefile:VinttTimeFile=getVinttTimeFile(path)

    if process not in timefile["trackedItems"]:
        timefile["trackedItems"][process]={
            "totalTime":0,
            "categoryTime":{}
        }

    timefile["trackedItems"][process]["totalTime"]+=time

    if not category in timefile["trackedItems"][process]["categoryTime"]:
        timefile["trackedItems"][process]["categoryTime"][category]=0

    timefile["trackedItems"][process]["categoryTime"][category]+=time

    writeTimeFile(timefile,path)

def getVinttTimeFile(path:str)->VinttTimeFile:
    """get vintt time file from location. return default if failed to find file"""

    try:
        with open(path,"r") as timefile:
            return safe_load(timefile)

    except:
        logger.warning("failed to find timefile at {}",path)

        return {
            "trackedItems":{}
        }

def writeTimeFile(timefile:VinttTimeFile,path:str)->None:
    """write to the timefile"""

    with open(path,"w") as timefilefile:
        timefilefile.write(safe_dump(timefile))