from fastapi import FastAPI, Depends,  HTTPException, status
from sqlalchemy.orm import Session
from auth_database import Base, get_db, engine
import models,schemas,utils
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


SECRET_KEY = "5kQkJ37dhPb_95k4Ij4RLZ1tqNn9Gzn3PBalrR9Ra9A"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20


#helper funtion that take user data

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encode_jwt

app = FastAPI()

@app.post("/signup")
def register_user(user : schemas.UserCreate, db: Session= Depends(get_db)):
    #check the user exit or not
    existing_user = db.query(models.User).filter(models.User.username ==  user.username).first()
    if existing_user:
        raise HTTPException(status_code = 400, detail = "Username already exist")

    #hash the pass
    hased_pass = utils.hash_password(user.password)

    # create new user instance
    new_user=models.User(
        username = user.username,
        email =  user.email,
        hashed_password= hased_pass,
        role = user.role
    )
    # save user in db
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    #return the value(exlude pass)
    return {'id' : new_user.id, "username": new_user.username, "role": new_user.role, "email" : new_user.email}


@app.post("/login")
def login(form_data : OAuth2PasswordRequestForm = Depends(), db : Session= Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid user name")

    if not utils.verify_password(form_data.password, user.hashed_password):

        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid password")

    token_data = {"sub" : user.username, "role" : user.role}

    token = create_access_token(token_data)
    return {"access_token" : token , "token_type" : "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token : str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "could not validate credential",
                                        headers = {"WWW-Authenticate" : "Bearer"}
                            )

    try:
        payload =jwt.decode(token, SECRET_KEY, algorithms= ALGORITHM)
        username : str = payload.get("sub")
        role : str = payload.get("role")
        if username is None or role is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    
    return {"username" : username, "role" :  role}

@app.get("/protected")
def protectd_route(current_user : dict = Depends(get_current_user)):
    
    return {"message" : f"Hello, {current_user["username"]} | You access a protected route" }    



def require_roles(allowed_roles : list[str]):
    def role_checker(current_user : dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail ="Not enough permission")

        return current_user
    return role_checker



@app.get("/profile")
def profile(current_user: dict = Depends(require_roles(["user", "admin"]))):
    return {"message" : f"profile of {current_user['username']} ({current_user['role']})"}


@app.get("/user/dashboard")
def user_dashboard(current_user : dict = Depends(require_roles(["user"]))):
    return {"message" : "Welcome User" }


@app.get("/admin/dashboard")
def user_dashboard(current_user : dict = Depends(require_roles(["admin"]))):
    return {"message" : "Welcome Admin" }

