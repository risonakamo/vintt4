from loguru import logger
from time import sleep

from vintt4.vintt_config import loadVinttConfig
from vintt4.process_watch import waitForProcess
from vintt4.vintt_time import incrementTime

from typing import List,Optional
from vintt4.types.vintt_config_types import VinttConfig,VinttTrackItem

WATCH_LOOP_INTERVAL_S:int=60

class VinttWatch:
    trackProcess:str
    category:str

    trackItem:VinttTrackItem

    timefile:str

    def __init__(self,configpath:str,timefile:str):
        config:VinttConfig=loadVinttConfig(configpath)

        watchProcesses:List[str]=list(config.trackItems.keys())

        logger.info("watching...")
        foundProcess:str=waitForProcess(watchProcesses)

        if not foundProcess in config.trackItems:
            logger.error("somehow found process was not on track item list")
            raise Exception("found process track list mismatch")

        logger.info("tracking: {}",foundProcess)

        self.trackProcess=foundProcess
        self.category="none"
        self.timefile=timefile
        self.trackItem=config.trackItems[foundProcess]

        self.watchLoop()

    def watchLoop(self)->None:
        """watch loop, writes to timefile at time interval"""

        while True:
            sleep(WATCH_LOOP_INTERVAL_S)

            logger.debug("writing to file")
            incrementTime(
                process=self.trackProcess,
                category=self.category,
                time=1,
                path=self.timefile
            )

    def changeCategory(self,category:str)->None:
        """change current track category"""

        if not category in self.trackItem.categories:
            logger.warning("changing to category not present in config: {}",category)

        self.category=category
