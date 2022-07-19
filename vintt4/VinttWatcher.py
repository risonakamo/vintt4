from loguru import logger
from time import sleep
from traceback import print_exc

from vintt4.vintt_config import loadVinttConfig
from vintt4.process_watch import waitForProcess
from vintt4.vintt_time import (incrementTime,addCategoryTimeDefaults,getVinttTimeFile,
    ensureProcessInTimefile)

from typing import List,Optional,Set
from vintt4.types.vintt_config_types import VinttConfig,VinttTrackItem
from vintt4.types.vintt_watch_types import CurrentWatch
from vintt4.types.vintt_time_types import VinttTimeFile

WATCH_LOOP_INTERVAL_S:int=60
"""seconds until adding 1 to the timefile. needs to be at 60 to be real time"""

DEFAULT_WATCH:CurrentWatch={
    "name":"",
    "currentTime":0,
    "currentCategory":"",
    "totalTime":0,
    "categoryTime":{}
}

class VinttWatch:
    trackProcess:Optional[str]
    category:str
    currentTime:int

    trackItem:Optional[VinttTrackItem]

    configpath:str
    timefile:str
    cachedTimefile:Optional[VinttTimeFile]

    config:Optional[VinttConfig]

    def __init__(self,configpath:str,timefile:str):
        self.trackProcess=None
        self.category="none"
        self.currentTime=0
        self.trackItem=None
        self.timefile=timefile
        self.cachedTimefile=None
        self.configpath=configpath
        self.config=None

    def computeWatchProcesses(self)->Set[str]:
        """load the vintt config and get the watch processes"""

        try:
            self.config=loadVinttConfig(self.configpath)

        except:
            logger.warning("load vintt config failed, fix config")
            print_exc()
            return set()

        return set(self.config.trackItems.keys())

    def watchForProcess(self)->None:
        """begin main logic. watch for process then begin the watch loop once found"""

        logger.info("watching...")
        foundProcess:str=waitForProcess(self.computeWatchProcesses)

        if not self.config:
            logger.error("completed wait for process, but missing config")
            raise Exception("no config")

        if not foundProcess in self.config.trackItems:
            logger.error("somehow found process was not on track item list")
            raise Exception("found process track list mismatch")

        logger.info("tracking: {}",foundProcess)

        self.trackProcess=foundProcess
        self.trackItem=self.config.trackItems[foundProcess]
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

        if not category in (self.trackItem.categories or []):
            logger.warning("changing to category not present in config: {}",category)

        self.category=category

    def getCurrentWatch(self)->CurrentWatch:
        """try to get current watch information"""

        # missing information, return default/empty current watch
        if not (self.trackProcess and self.cachedTimefile and self.trackItem):
            return DEFAULT_WATCH

        return {
            "name":self.trackItem.displayName,
            "currentTime":self.currentTime,
            "currentCategory":self.category,
            "totalTime":self.cachedTimefile["trackedItems"][self.trackProcess]["totalTime"],
            "categoryTime":addCategoryTimeDefaults(
                self.cachedTimefile["trackedItems"][self.trackProcess]["categoryTime"],
                self.trackItem.categories or []
            )
        }