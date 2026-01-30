from fastapi import APIRouter


router = APIRouter()

@router.get('/users/', tags = ['users'])
def get_users():
    return [{'username':'Bob'},{'username':'Alice'}]

@router.get('/users/me', tags = ['users'])
def read_get_me():
    return [{'username':'current_user'}]