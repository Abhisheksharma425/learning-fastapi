from pydantic import BaseModel, Field
from typing import Optional

class Item(BaseModel):
    name: str
    description: Optional[dict] = None
    price: float = Field(gt = 0, description='price must be greater than zero')
    tax: float = 0.1