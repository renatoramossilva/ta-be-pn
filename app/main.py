"""
Main module for the FastAPI application.
"""

from fastapi import FastAPI  # type: ignore  # pylint: disable=import-error

from app.routes import router

app = FastAPI()

app.include_router(router)


@app.get("/")
def home():
    """
    Welcome message for the API.
    """
    return {"message": "Welcome to mobile network coverage API"}
