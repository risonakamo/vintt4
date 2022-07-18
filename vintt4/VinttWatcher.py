from loguru import logger
from time import sleep

from vintt4.vintt_config import loadVinttConfig
from vintt4.process_watch import waitForProcess
from vintt4.vintt_time import (incrementTime,addCategoryTimeDefaults,getVinttTimeFile,
    ensureProcessInTimefile)

from typing import List,Optional
from vintt4.types.vintt_config_types import VinttConfig,VinttTrackItem
from vintt4.types.vintt_watch_types import CurrentWatch
from vintt4.types.vintt_time_types import VinttTimeFile

WATCH_LOOP_INTERVAL_S:int=10

class VinttWatch:
    trackProcess:Optional[str]
    category:str
    currentTime:int

    trackItem:Optional[VinttTrackItem]

    configpath:str
    timefile:str
    cachedTimefile:Optional[VinttTimeFile]

    def __init__(self,configpath:str,timefile:str):
        self.trackProcess=None
        self.category="none"
        self.currentTime=0
        self.trackItem=None
        self.timefile=timefile
        self.cachedTimefile=None
        self.configpath=configpath

    def watchForProcess(self)->None:
        """begin main logic. watch for process then begin the watch loop once found"""

        config:VinttConfig=loadVinttConfig(self.configpath)

        watchProcesses:List[str]=list(config.trackItems.keys())

        logger.info("watching...")
        foundProcess:str=waitForProcess(watchProcesses)

        if not foundProcess in config.trackItems:
            logger.error("somehow found process was not on track item list")
            raise Exception("found process track list mismatch")

        logger.info("tracking: {}",foundProcess)

        self.trackProcess=foundProcess
        self.trackItem=config.trackItems[foundProcess]
        self.cachedTimefile=ensureProcessInTimefile(
            getVinttTimeFile(self.timefile),
            foundProcess
        )

        self.watchLoop()

    def watchLoop(self)->None:
        """watch loop, writes to timefile at time interval"""

        while True:
            sleep(WATCH_LOOP_INTERVAL_S)

            if not self.trackProcess:
                raise Exception("watch loop but no track process")

            logger.debug("writing to file")
            self.cachedTimefile=incrementTime(
                process=self.trackProcess,
                category=self.category,
                time=1,
                path=self.timefile
            )
            self.currentTime+=1

    def changeCategory(self,category:str)->None:
        """change current track category"""

        if not self.trackItem:
            logger.warning("tried to change category but no process being tracked")
            return

        if not category in self.trackItem.categories:
            logger.warning("changing to category not present in config: {}",category)

        self.category=category

    def getCurrentWatch(self)->CurrentWatch:
        """try to get current watch information"""

        # missing information, return default/empty current watch
        if not (self.trackProcess and self.cachedTimefile and self.trackItem):
            return {
                "name":"",
                "currentTime":0,
                "currentCategory":"",
                "totalTime":0,
                "categoryTime":{}
            }

        return {
            "name":self.trackItem.displayName,
            "currentTime":self.currentTime,
            "currentCategory":self.category,
            "totalTime":self.cachedTimefile["trackedItems"][self.trackProcess]["totalTime"],
            "categoryTime":addCategoryTimeDefaults(
                self.cachedTimefile["trackedItems"][self.trackProcess]["categoryTime"],
                self.trackItem.categories
            )
        }