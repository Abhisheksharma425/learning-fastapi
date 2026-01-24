from fastapi import FastAPI
from typing import Optional

from pydantic import BaseModel

app =FastAPI()


@app.get("/")
def read_root():
    return {"message" : "Hello World"}


@app.get("/greet")
def greet():
    return {"message" : "Hello sam"}

#Below is example of path parameter and query parameter.
#Here name is path paremeter and age is query parameter.
# http://127.0.0.1:8000/greet/Krishn?age=30
@app.get("/greet/{name}")
def greet_name(name: str, age: Optional[int]=None):
    return {"message" : f"Hello {name} and you are {age} years old "}

# http://127.0.0.1:8000/greet/?name=kk&age=15
# example of only query parameter
@app.get("/greet/")
def greet_name(name: str, age: Optional[int]=None):
    return {"message" : f"Hello {name} and you are {age} years old "}



class Student(BaseModel):
    name : str
    age : int
    roll : int

@app.post("/create_student")
def create_student(student : Student):
    return {
        "name" : student.name,
        "age"  : student.age,
        "roll" : student.roll
    }


    
