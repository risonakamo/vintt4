from typing import TypedDict,Dict

class VinttTimeFile(TypedDict):
    """time file storage"""

    trackedItems:Dict[str,"VinttTime"]
    """time information for each tracked item. key: process name, val: time information"""

class VinttTime(TypedDict):
    """time information for a process"""

    totalTime:int
    """total time of the process (s)"""

    categoryTime:Dict[str,int]
    """time per category. key: category name, val: the time (s)"""