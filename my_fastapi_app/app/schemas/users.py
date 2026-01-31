from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.schemas.items import Item

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password:str

class User(UserBase):
    id:int
    is_active:bool
    items: List[Item] =[]
    
    class Config:
        from_attributes = True