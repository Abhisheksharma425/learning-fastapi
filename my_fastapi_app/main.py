from fastapi import FastAPI, Depends
from app.routers import items, users
from app.dependencies import verify_token
import logging
from app.routers import users, items
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)
logging.basicConfig(level = logging.INFO, format = "%(asctime)s - %(levelname)s -%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)


app = FastAPI()


app.include_router(items.router, prefix="/items",dependencies=[Depends(verify_token)])
app.include_router(users.router, prefix="/users")
print(items.router)
@app.get('/')
def root():
    logger.info("Root endpoint accessed")
    return {'message':'Hello World'}