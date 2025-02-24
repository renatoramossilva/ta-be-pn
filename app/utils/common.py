"""
Common functions used in the project
"""

# pylint: disable=import-error

import pyproj  # type: ignore
import requests

from app.utils.logger import setup_logger

# Timeout for the requests in seconds
REQUEST_TIMEOUT = 10

LOG = setup_logger(__name__)


def wgs84_to_lamber93(lat: float, lon: float) -> tuple[float, float]:
    """
    Convert WGS84 coordinates to Lamber93 coordinates.

    WGS84 (World Geodetic System 1984) is a global coordinate system used by GPS,
    which provides a standard for mapping and navigation worldwide.

    Lambert93 is a coordinate system used in France, which is based
    on the Lamber Conformal Conic projection.

    **Request Body:**
    - `lat`: Latitude in GPS coordinates
    - `lon`: Longitude in GPS coordinates

    **Returns:**
    A tuple containing the Lambert93 x and y coordinates
    """
    LOG.info("Converting WGS84 coordinates to Lamber93")
    wgs84 = pyproj.Proj(init="epsg:4326")
    lamber93 = pyproj.Proj(init="epsg:2154")

    LOG.info("wgsr84: %s(latitude), %s(longitude)", lat, lon)
    x, y = pyproj.transform(wgs84, lamber93, lon, lat)

    LOG.info("lamber93: %s(x), %s(y)", x, y)

    return x, y


def lamber93_to_wgs84(coord_x: float, coord_y: float) -> tuple[float, float]:
    """
    Convert Lamber93 coordinates to WGS84 coordinates.

    Lamber93 is a coordinate system used in France, which is based
    on the Lamber Conformal Conic projection.
    It is designed for accurate mapping of the French territory.

    WGS84 (World Geodetic System 1984) is a global coordinate system used by GPS,
    which provides a standard for mapping and navigation worldwide.

    **Request Body:**
    - `coord_x`: Lamber 93 x coordinate
    - `coord_y`: Lamber 93 y coordinate

    **Request Body:**
    A tuple containing the longitude and latitude in GPS coordinates
    """
    LOG.info("Converting Lamber93 coordinates to WGS84")
    lamber = pyproj.Proj(
        "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 "
        "+x_0=700000 +y_0=6600000 +ellps=GRS80 "
        "+towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
    )

    wgs84 = pyproj.Proj("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")

    LOG.info("lamber93: %s (x), %s (y)", coord_x, coord_y)
    lat, long = pyproj.transform(lamber, wgs84, coord_x, coord_y)

    LOG.info("wgsr84: %s (latitude), %s (longitude)", lat, long)
    return lat, long


def get_coordinates(address: str) -> tuple[float, float] | None:
    """
    Get the coordinates of an address

    **Request Body:**
    - `address`: The address to get the coordinates from

    **Returns:**
    A tuple containing the longitude and latitude of the address
    e.g.: [<longitude>, <latitude>]

    **Raises:**
    - `requests.exceptions.Timeout`: If the request times out
    - `Exception`: If an error occurs while fetching the coordinates
    """
    url = f"https://api-adresse.data.gouv.fr/search/?q={address}"

    LOG.info("Fetching coordinates for address: %s", address)
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        data = response.json()

        if data.get("features"):  # Check if the features key exists
            coordinates = data["features"][0]["geometry"]["coordinates"]
            LOG.info("Coordinates found: %s", coordinates)
            return coordinates

    except requests.exceptions.Timeout:
        LOG.error(
            "Timeout occurred while fetching coordinates for address: %s", address
        )

    except Exception as ex:  # pylint: disable=broad-except
        LOG.error("An error occurred while fetching coordinates: %s", ex)

    return None
