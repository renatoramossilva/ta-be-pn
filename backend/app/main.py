"""
Main module for the FastAPI application.
"""

from fastapi import FastAPI  # type: ignore  # pylint: disable=import-error
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router
from app.utils.logger import setup_logger

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


LOG = setup_logger(__name__)


@app.get("/")
def home():
    """
    Welcome message for the API.
    """
    LOG.info("Welcome message returned")
    return {"message": "Welcome to mobile network coverage API"}
