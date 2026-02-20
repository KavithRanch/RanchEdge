from typing import Annotated

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from datetime import datetime

# Create FastAPI instance
app = FastAPI()


class Person(BaseModel):
    name: str
    age: int
    birthday: datetime


# Endpoint to determine whether responses are working
@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/name")
def greeting(name: Annotated[list[str], Query(max_length=2)]):
    return {"greeting": f"Hello, {name[0]} {name[1]}!"}


@app.get("/add")
def add_numbers(a: int = 3, b: int = 7):
    return {"result": f"{a} + {b} = {a + b}"}


@app.get("/person", response_model=Person)
def generate_person(name: str, age: int, birthday: datetime):
    return {"name": name, "age": age, "birthday": birthday}


@app.post("/person")
def generate_username(person: Person):
    return {"username": f"{person.name}{person.birthday.strftime('%d')}"}


class Hobby(BaseModel):
    activity: str
    hours: int


@app.post("/hobbies")
def return_hobbies(person: Person, hobby: Hobby):
    return {
        "message": f"{person.name} likes {hobby.activity} and usually plays for {hobby.hours} hours"
    }
