from fastapi import FastAPI

# Create FastAPI instance
app = FastAPI()


# Endpoint to determine whether responses are working
@app.get("/health")
def health_check():
    return {"status": "healthy"}
