"""
Common functions used in the project
"""

# pylint: disable=import-error

import logging

import pyproj  # type: ignore
import requests

# Timeout for the requests in seconds
REQUEST_TIMEOUT = 10

LOG = logging.getLogger(__name__)


def lamber93_to_wgs84(coord_x: float, coord_y: float) -> tuple[float, float]:
    """
    Convert Lambert93 coordinates to WGS84 coordinates.

    Lambert93 is a coordinate system used in France, which is based
    on the Lambert Conformal Conic projection.
    It is designed for accurate mapping of the French territory.

    WGS84 (World Geodetic System 1984) is a global coordinate system used by GPS,
    which provides a standard for mapping and navigation worldwide.

    **Request Body:**
    - `coord_x`: Lambert 93 x coordinate
    - `coord_y`: Lambert 93 y coordinate

    **Request Body:**
    A tuple containing the longitude and latitude in GPS coordinates
    """
    lambert = pyproj.Proj(
        "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 "
        "+x_0=700000 +y_0=6600000 +ellps=GRS80 "
        "+towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
    )

    wgs84 = pyproj.Proj("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
    long, lat = pyproj.transform(lambert, wgs84, coord_x, coord_y)
    return long, lat


def get_coordinates(address: str) -> tuple[float, float] | None:
    """
    Get the coordinates of an address

    **Request Body:**
    - `address`: The address to get the coordinates from

    **Returns:**
    A tuple containing the longitude and latitude of the address

    **Raises:**
    - `requests.exceptions.Timeout`: If the request times out
    - `Exception`: If an error occurs while fetching the coordinates
    """
    url = f"https://api-adresse.data.gouv.fr/search/?q={address}"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        data = response.json()

        if data.get("features"):  # Check if the features key exists
            return data["features"][0]["geometry"]["coordinates"]

    except requests.exceptions.Timeout:
        LOG.error(
            "Timeout occurred while fetching coordinates for address: %s", address
        )

    except Exception as ex:  # pylint: disable=broad-except
        LOG.error("An error occurred while fetching coordinates: %s", ex)

    return None
