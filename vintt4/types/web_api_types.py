from pydantic import BaseModel

class SetCategoryReq(BaseModel):
    """request to change category"""

    category:str