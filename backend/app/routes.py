"""
This module contains the FastAPI routes for the mobile network coverage API.
"""

# pylint: disable=import-error

from fastapi import APIRouter, HTTPException  # type: ignore

from app.db.data import find_network_coverage
from app.utils.common import get_coordinates
from app.utils.logger import setup_logger

router = APIRouter()

LOG = setup_logger(__name__)


@router.get("/coverage")
def coverage(
    address: str,
) -> dict[str, dict[str, bool]]:
    """
    Get network coverage for a given address

    **Request Body:**
    - `address`: The address to get the network coverage for

    **Returns:**
    A dictionary containing the list of operators and their coverage
        for the given address
    """
    LOG.info("Getting network coverage for address %s: address")
    coordinates = get_coordinates(address)

    if coordinates is None:
        LOG.error("Unable to get coordinates for the given address")
        raise HTTPException(
            status_code=400, detail="Unable to get coordinates for the given address"
        )

    data_coverage = find_network_coverage(*coordinates)

    if not data_coverage:
        LOG.error("Unable to find network coverage for the given location")
        raise HTTPException(
            status_code=400,
            detail="Unable to find network coverage for the given location",
        )

    return data_coverage
