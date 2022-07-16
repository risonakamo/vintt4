from psutil import process_iter,Process
from time import sleep

from typing import List,Set

def waitForProcess(processes:List[str])->str:
    """wait for process in given list to exist. returns the found process"""

    processSet:Set[str]=set(processes)

    while True:
        for process in process_iter():
            process:Process

            if process.name() in processSet:
                return process.name()

        sleep(2)

    raise Exception("escaped while loop")