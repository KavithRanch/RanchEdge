"""
This is the main entry point for the FastAPI application.
It sets up the application instance, includes the necessary routers, and defines a health check endpoint.

Author: Kavith Ranchagoda
Last Updated:
"""

from fastapi import FastAPI
from app.api.v1 import ev_opportunities_router

# Create FastAPI instance
app = FastAPI()

# Include the EV opportunities router
app.include_router(ev_opportunities_router)


# Endpoint to determine whether responses are working
@app.get("/health")
def health_check():
    return {"status": "healthy"}
