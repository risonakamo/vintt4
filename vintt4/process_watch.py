from psutil import process_iter,Process
from time import sleep

from typing import List,Set,Union,Callable

WaitProcessesCallback=Callable[[],Set[str]]
"""callback the produces a list of processes to wait for. should return a set of processes"""

def waitForProcess(processesCallback:WaitProcessesCallback)->str:
    """uses given processes callback to create a list of processes (actually a set).
    checks if any of the processes in that set exist, if it does, then return the name
    of that process. the process callback gets called each wait cycle"""

    while True:
        processSet:Set[str]=processesCallback()

        for process in process_iter():
            process:Process

            if process.name() in processSet:
                return process.name()

        sleep(2)

    raise Exception("escaped while loop")