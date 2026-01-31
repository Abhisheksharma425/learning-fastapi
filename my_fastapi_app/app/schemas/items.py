from pydantic import BaseModel
from typing import Optional, List

class ItemBase(BaseModel):
    title:str
    description:Optional[str]=None

class ItemCreate(BaseModel):
    pass

class Item(ItemBase):
    id:int
    owner_id:int

    class Config:
        from_attributes = True