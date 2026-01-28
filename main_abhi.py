from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from contextlib import asynccontextmanager


ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Loading AI Model from disk')

    fake_model = lambda x:x*100

    ml_models['house_model'] = fake_model
    print('Model Loaded sucessfully')
    yield
    print("shutting down and cleaning up ")
    ml_models.clear()

app_main = FastAPI(title='My AI Model API', lifespan=lifespan)

# @app_main.get('/')
# def home():
#     return {'cat':'message is pretty clear','joker':['ab','abhi']}


# @app_main.get('/match')
# def match():
#     return {'message':'24 matches present'}

# @app_main.get('/match/')
# def match():
#     return {'message':'2 matches present'}

class HousePrice(BaseModel):
    sqft: float
    bedrooms: int
    has_garden: bool = False


@app_main.get('/health')
def health():
    return {'status':'running','message':'AI Service is active'}

@app_main.post('/predict')
def predict_price(input_data: HousePrice): #input_data 
    model = ml_models.get("house_model")
    if not model:
        return {"error":"Model not found"}
    estimated_price = model(input_data.sqft)
    print(f"Received Data: {input_data}")
    return {
        "details":"Calculated using the efficient loaded model",
        "estimated_price": estimated_price
    }