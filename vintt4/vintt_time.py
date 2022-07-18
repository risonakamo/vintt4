from yaml import safe_load,safe_dump
from loguru import logger

from typing import List,Set
from vintt4.types.vintt_time_types import VinttTimeFile,CategoryTime

def incrementTime(
    process:str,
    category:str,
    time:int,
    path:str
)->VinttTimeFile:
    """increment a process's time in a category. writes to the time file. returns the updated
    timefile"""

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

    return timefile

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

def addCategoryTimeDefaults(categorytime:CategoryTime,categories:List[str])->CategoryTime:
    """given a list of categories, add these categories to a category time if they dont already
    exist on the category time"""

    newcattime:CategoryTime={}

    combinedcategories:Set[str]=set(categories)|set(categorytime.keys())

    for category in combinedcategories:
        category:str

        if category in categorytime:
            newcattime[category]=categorytime[category]

        else:
            newcattime[category]=0

    return newcattime

def ensureProcessInTimefile(timefile:VinttTimeFile,process:str)->VinttTimeFile:
    """modify timefile to include the specified process, if not existing"""

    if process not in timefile["trackedItems"]:
        timefile["trackedItems"][process]={
            "totalTime":0,
            "categoryTime":{}
        }

    return timefile