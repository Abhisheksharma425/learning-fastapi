from fastapi import FastAPI
from app.routers import items, users



app = FastAPI()


app.include_router(items.router)
app.include_router(users.router)
print(items.router)
@app.get('/')
def root():
    return {'message':'Hello World'}