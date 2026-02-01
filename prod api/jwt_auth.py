import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

app = FastAPI()

# --- CONFIGURATION (The "Secrets") ---
SECRET_KEY = "my_super_secret_key" # The stamp we put on the token
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- SECURITY TOOLS ---
# 1. The Hasher: Turns "secret" into "$2b$12$..."
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. The Extractor: Knows how to read the token from the "Authorization" header
# This also creates the "Authorize" button in Swagger UI!
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- FAKE DATABASE ---
# In real life, this is your SQL DB. Here, it's just a dictionary.
fake_users_db = {}

# --- HELPER FUNCTIONS ---

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- THE DEPENDENCY (The Bouncer) ---
# This runs before every protected route.
# It takes the token, decodes it, and checks if it's valid.
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 1. Decode the token using our SECRET_KEY
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # "sub" is where we stored the username
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # 2. Check if user actually exists in DB
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return user

# --- MODELS ---
class UserSignup(BaseModel):
    username: str
    password: str

# --- ROUTES ---

@app.post("/signup")
def signup(user: UserSignup):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # CRITICAL: We NEVER save the plain password. We save the hash.
    hashed_pw = get_password_hash(user.password)
    
    fake_users_db[user.username] = {
        "username": user.username,
        "hashed_password": hashed_pw
    }
    return {"msg": "User created! You can now login."}

@app.post("/login")
# OAuth2PasswordRequestForm is a special FastAPI class that expects
# "username" and "password" as form data, not JSON.
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Verify: Does the password they sent match the hash we stored?
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    # Issue Token
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/vault")
def open_vault(current_user: dict = Depends(get_current_user)):
    return {
        "message": "Welcome to the vault!",
        "gold_bars": 100,
        "user_logged_in": current_user["username"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)