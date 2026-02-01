from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import verify_token
from sqlalchemy.orm import Session
from typing import List

from app import models
from app.schemas import users as user_schema
from app.dependencies import get_db


router = APIRouter()

# @router.get('/', tags = ['users'])
# def get_users(x_token:str = Depends(verify_token)):
#     return [{'username':'Bob'},{'username':'Alice'}]

# @router.get('/me', tags = ['users'])
# def read_get_me():
#     return [{'username':'current_user'}]

@router.post('/', response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    fake_hashed_password = user.password +"ab"
    new_user = models.User(email = user.email, hashed_password = fake_hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/', response_model=List[user_schema.User])
def read_users(skip: int = 0, limit:int = 10, db:Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users
