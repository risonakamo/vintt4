from __future__ import annotations
from pydantic import BaseModel

from typing import TypedDict,Dict,List

class VinttTrackItem(BaseModel):
    """item to be tracked"""

    displayName:str
    categories:List[str]
    """list of categories for the track item"""

class VinttConfig(BaseModel):
    """configuration for vintt"""

    trackItems:Dict[str,VinttTrackItem]
    """items to be tracked. key: process name. val: track item configuration for the process"""