from fastapi import FastAPI, Depends
from database import Base, get_db, engine
from sqlalchemy.orm import Session
import model
from pydantic import BaseModel

app= FastAPI()

class Bookstore(BaseModel):
    id:int
    title:str
    author:str
    publish_date:str

@app.post("/books")
def creat_book(book: Bookstore, db: Session= Depends(get_db)):
    
    new_book = model.Book(id=book.id, title=book.title, author= book.author, publish_date=book.publish_date)
    db.add(new_book)
    try:
        db.commit()
        db.refresh(new_book)
        return new_book
      
    except Exception as e:
        db.rollback()
        raise e
@app.get("/book")
def get_book(db: Session= Depends(get_db)):
    books = db.query(model.Book).all()
    return books     
      