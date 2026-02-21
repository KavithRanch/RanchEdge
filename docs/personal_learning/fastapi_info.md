# FastAPI
This documentation serves as a quick reminder to myself of FastAPI basics

---
## Purpose
FastApi is a python framework which helps serve REST Apis quicky and effectively

## Benefits
- [x] Fast performance due to asynchronous ability
- [x] Automatic API documentation generation (Swagger UI)
- [x] Request bodies are validated before hitting logic so that less runtime bugs occur using Pydantic

## Basic Usage
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def return_status():
    return { "status" : "good" }
```

## Notes
### Parameters
* If additional data, validations or examples to display are needed for a certain param we can use Query(metadata) or Path(metadata) to do so
- [ ] Routes are checked in order and the first valid matching route will be applied
```python
@app.get("/name/{name}")
def greeting(name: str):
    return {"greeting": f"Hello, {name}"}

@app.get("/name/me")
def greeting(name: str):
    return {"greeting": f"Hello, Kavith"}

# Request path => /name/me | Response => {"greeting": "Hello, me"}
```
- [ ] When declaring function parameters that aren't in path, they are assumed to be query params
```python
@app.get("/add")
def add_numbers(a: int, b: int):
    return {"result": f"{a} + {b} = {a + b}"}

@app.get("/add")
def add_numbers(a: int = 3, b: int = 7): # If no params sent, it will default to given values
    return {"result": f"{a} + {b} = {a + b}"} 

# Request path => /add/?a=3&b=7 OR /add | Both respond with => {"result": "3 + 7 = 10"}
```

- [ ] Optional parameters can be set by defaulting to None. Required parameters are declared by just putting it in the function params but not assigning a value
```python
@app.get("/add")
def add_numbers(a: int = 3, b: int = 7, c: int | None = None): # If no params sent, it will default to given values
    if c:
        return {"result": f"{a} + {b} + {c} = {a + b + c}"} 
    return {"result": f"{a} + {b} = {a + b}"} 

# Request path => /add/?a=3&b=7&c=2 | Response => {"result": "3 + 7 + 2 = 12"}
# Request path => /add/?a=3&b=7 | Response => {"result": "3 + 7 = 10"}
```

- [ ] Validating path and query parameters especially strings can be done with Path/Query(validations...) function from fastapi and Annotated[type(s), Path/Query()] from typing
    - The Path parameters must be required
```python
from fastapi import Query, Path
from typing import Annotated

@app.get("/name/{first_name}")
def greeting(first_name: Annotated[str, Path(min_length=3, max_length=50)], last_name: Annotated[str | None, Query(min_length=3, max_length=50)] = None):
    return {"greeting": f"Hello, {first_name} {last_name}"}
```

- [ ] We can send an array of items as a param. For an array 'arr' we need to do ?arr=item1&arr=item2&arr=item3 respectfully
```python
from fastapi import Query
from typing import Annotated

@app.get("/name")
def greeting(name: Annotated[list[str], Query(max_length=2)]):
    return {"greeting": f"Hello, {name[0]} {name[1]}"}

# Path => /name/?name=Kavith&name=Ranchagoda | Response => {"greeting": "Hello, Kavith Ranchagoda"}
```

### Request/Response Bodies
- [ ] Request and Response bodies are defined using the Pydantic Library's BaseModel
```python
from pydantic import BaseModel
from datetime import datetime

class Person(BaseModel):
    name: str
    age: int
    birthday: datetime

# Having the Person Class as a param, ensures Pydantic validates the input matches the model
# Else return a 422 Validation Error
@app.post("/person")
def generate_username(person: Person): 
    return {"username": f"{person.name}{person.birthday.strftime('%d')}"}

# Having the response_model=Person ensures any return values must match the shape of Person
# If more values are returned, then it strips the extra to match Person
# If less values are returned, an 500 Internal Server Error is thrown
@app.get("/person", response_model=Person)
def generate_person(name: str, age: int, birthday: datetime):
    return {
        "name": name,
        "age": age,
        "birthday": birthday,
    }
```

- [ ] We can send multiple request bodies at once 
```python
from pydantic import BaseModel
from datetime import datetime

class Person(BaseModel):
    name: str
    age: int
    birthday: datetime

class Hobby(BaseModel):
    activity: str
    hours: int

@app.post("/hobbies")
def return_hobbies(person: Person, hobby: Hobby):
    return {"message": f"{person.name} likes {hobby.activity} and usually plays for {hobby.hours} hours"}
```

- [ ] We can also nested Pydantic Models but always list the nested ones first so the following models recognize it exists
```python
from pydantic import BaseModel
from datetime import datetime

class Hobby(BaseModel):
    activity: str
    hours: int

class Person(BaseModel):
    name: str
    age: int
    birthday: datetime
    hobbies: list[Hobby] = []
```

### Routers
When organizing endpoints by services in seperate files, it requires the use of routers to relate them back and make them recognizable within main.py
* Per service we would create the router:
```python
# First Service File
router = APIRouter(prefix='/api/v1/example1')

@router.get("/people")
def get_people():
    return "Person"

# Second Service File
router = APIRouter(prefix='/api/v1/example2')

@router.get("/games")
def get_games():
    return "Games"
```
* Then within main.py we register the routers:
```python
from first_service_file import router as first_router
from second_service_file import router as second_router

app.include_router(first_router)
app.include_router(second_router)
```


