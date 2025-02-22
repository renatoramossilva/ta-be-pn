"""
This module contains the models for the application
"""

from pydantic import BaseModel


class CoverageResponse(BaseModel):
    """
    Response model for the get_coverage route

    :param `coordinates`: The coordinates of the address
    :param `gps`: The GPS coordinates of the address
    """

    coordinates: list[float]
    gps: tuple[float, float]
