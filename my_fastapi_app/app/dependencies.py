import logging
from fastapi import Header, HTTPException
from app.database import SessionLocal
logger = logging.getLogger(__name__)

def common_pagination(skip:int = 0, limit:int = 20):
    return {'skip':skip,'limit':limit}

def verify_token(x_token:str = Header(None)):
    if x_token !='777':
        logger.warning("Some fraud tried to login")
        raise HTTPException(status_code=403, detail = "Go away you fraud!!")
    logger.info("Access Granted")
    return x_token

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()