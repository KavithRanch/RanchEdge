# FastAPI
This documentation serves as a quick reminder to myself of FastAPI basics

---
## Purpose
FastApi is a python framework which helps serve REST Apis quicky and effectively

## Benefits
- [x] Fast performance due to asynchronous ability
- [x] Automatic API documentation generation (Swagger UI)
- [x] Request bodies are validated before hitting logic so that less runtime bugs occur

## Basic Usage
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/route")
def return_status():
    return { "status" : "good" }
```