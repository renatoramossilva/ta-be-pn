"""
Main module for the FastAPI application.
"""

from fastapi import FastAPI  # type: ignore  # pylint: disable=import-error

from app.routes import router
from app.utils.logger import setup_logger

app = FastAPI()

app.include_router(router)


LOG = setup_logger(__name__)


@app.get("/")
def home():
    """
    Welcome message for the API.
    """
    LOG.info("Welcome message returned")
    return {"message": "Welcome to mobile network coverage API"}
