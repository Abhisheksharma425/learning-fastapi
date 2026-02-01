from pydantic import BaseModel

# The "Full" data inside our database
class UserInDB(BaseModel):
    username: str
    hashed_password: str
    internal_notes: str = "This user is a VIP"

# The "Public" data we want to show the world
class UserPublic(BaseModel):
    username: str
from fastapi import FastAPI

app = FastAPI()

# Simulated database record
fake_user_db = {
    "username": "coder_99",
    "hashed_password": "secret_hash_123",
    "internal_notes": "Needs a discount"
}

@app.get("/user/profile", response_model=UserPublic)
def get_user_profile():
    # We are returning the WHOLE dictionary (with email and password)
    # BUT, FastAPI will "filter" it through UserPublic
    return fake_user_db