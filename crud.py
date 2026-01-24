from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

books = [
    {
        "id" : 1,
        "title" : "The alchemist",
        "author" : "Paulo Coelho",
        "publish_date" : "1988-01-01" 
    
    },

    {
        "id" : 2,
        "title" : "The god of small thing",
        "author" : "Arundhati Roy",
        "publish_date" : "1991-04-04" 

    },

     {
        "id" : 3,
        "title" : "The white tiger",
        "author" : "Arvinda Adig",
        "publish_date" : "2008-01-01" 

    },

     {
        "id" : 4,
        "title" : "The Palace of Illusion",
        "author" : "Chitra Banarjee",
        "publish_date" : "2008-02-12" 

    }

]

app = FastAPI()


@app.get("/book")
def get_book():
    return books


@app.get("/book/{book_id}")
def get_book(book_id : int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Book Not found")



class Book(BaseModel):
    id : int
    title : str
    author : str
    publish_date : str

@app.post("/book")   
def  create_book(book : Book):
    new_book=book.model_dump()
    books.append(new_book)

class BookUpdate(BaseModel):
    title : str
    author : str
    publish_date : str


@app.put("/book/{book_id}")
def update_book(book_id : int, book_update: BookUpdate):
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_update.title
            book["author"] = book_update.author
            book["publish_date"] = book_update.publish_date
            
            return book
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Book Not Found")


@app.delete("/book/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message" : "Book Deleted "}
            
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Book Not Found")        


    


