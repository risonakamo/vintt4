from typing import TypedDict,Dict,List

class VinttConfig(TypedDict):
    """configuration for vintt"""

    trackItems:Dict[str,"VinttTrackItem"]
    """items to be tracked. key: process name. val: track item configuration for the process"""

class VinttTrackItem(TypedDict):
    """item to be tracked"""

    displayName:str
    categories:List[str]
    """list of categories for the track item"""