from fastapi import FastAPI, HTTPException
from typing import List
from schemas import Item

db = []

app = FastAPI()

@app.post('/items/', response_model=Item)
def create_item(item: Item):
    db.append(item)
    return item

@app.get('/items/{items_id}')
def read_items(items_id: int, q: str = None):
    if items_id>=len(db):
        raise HTTPException(status_code=404, detail="Item not found")
    return {'items':db[items_id], "query":q}

# GET: Query Parameters (filtering)
@app.get("/items/", response_model=List[Item])
def list_items(limit: int = 10):
    print(db)
    return db[:limit]

@app.get("/buy/")
def check_out(items: str):
    return {'items':items} #http://127.0.0.1:8000/buy/?items=shirt -- > example