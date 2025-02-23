"""
This module contains the FastAPI routes for the mobile network coverage API.
"""

# pylint: disable=import-error

from fastapi import APIRouter  # type: ignore

from app.db.data import find_network_coverage
from app.utils import get_coordinates

router = APIRouter()


@router.get("/coverage")
def coverage(address: str) -> dict[str, dict[str, bool]]:
    """
    Get network coverage for a given address

    **Request Body:**
    - `address`: The address to get the network coverage for

    **Returns:**
    A dictionary containing the list of operators and their coverage
        for the given address
    """
    cood = get_coordinates(address)
    if cood is None:
        return {"error": "Unable to get coordinates for the given address"}, 400

    return find_network_coverage(*cood)
