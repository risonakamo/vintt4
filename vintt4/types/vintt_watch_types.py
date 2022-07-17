from typing import TypedDict,Dict

class CurrentWatch(TypedDict):
    """current watch information"""

    name:str
    """if empty, then there is no current watch (all other fields disregarded)"""

    currentTime:int
    currentCategory:str

    totalTime:int
    categoryTime:Dict[str,int]
    """key: category name, val: time for that category"""