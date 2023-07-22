from pydantic import BaseModel

class SetCategoryReq(BaseModel):
    """request to change category"""

    category:str

class NewCategoryReq(BaseModel):
    """request new category to be added"""

    categoryName:str