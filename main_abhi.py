from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app_main = FastAPI()

@app_main.get('/')
def home():
    return {'cat':'message is pretty clear','joker':['ab','abhi']}


@app_main.get('/match')
def match():
    return {'message':'24 matches present'}

@app_main.get('/match/')
def match():
    return {'message':'2 matches present'}