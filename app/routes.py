"""
This module contains the FastAPI routes for the mobile network coverage API.
"""

# pylint: disable=import-error

from fastapi import APIRouter  # type: ignore

from app.models import CoverageResponse  # type: ignore
from app.utils import get_coordinates, lamber93_to_wgs84

router = APIRouter()


@router.get("/coverage", response_model=CoverageResponse)
def get_coverage(address: str) -> CoverageResponse | tuple[dict[str, str], int]:
    """
    Get network coverage for a given address

    :param address: The address to get the network coverage for

    :return: A dictionary containing the list of operators and their coverage
        for the given address
    """
    cood = get_coordinates(address)
    if cood is None:
        return {"error": "Unable to get coordinates for the given address"}, 400

    gps_coodinates = lamber93_to_wgs84(*cood)

    return CoverageResponse(coordinates=get_coordinates(address), gps=gps_coodinates)
