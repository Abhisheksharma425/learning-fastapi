from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app_main = FastAPI(title='My AI Model API')

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
    print(f"Received Data: {input_data}")
    return {
        "input_received": input_data,
        "estimated_price": 25000
    }