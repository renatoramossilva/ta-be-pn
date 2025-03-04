"""
This file contains tests for the utils module.
"""

import pytest
import requests

from app.utils.common import get_coordinates, lamber93_to_wgs84, request_external_api


@pytest.mark.parametrize(
    "coord_x, coord_y, expected_long, expected_lat",
    [
        (102980, 6847973, -5.08885611530134, 48.4565745588299),
        (239371, 6727955, -3.123743901548036, 47.49112341534302),
        (347852, 6780916, -1.7276049268683342, 48.033722330459035),
        (1240585, 6154019, 9.550389050940431, 42.28436027507253),
    ],
)
def test_lamber93_to_wgs84(coord_x, coord_y, expected_long, expected_lat):
    """
    Test the lamber93_to_wgs84 function

    :param coord_x: The Lambert 93 x coordinate
    :param coord_y: The Lambert 93 y coordinate
    :param expected_long: The expected longitude
    :param expected_lat: The expected latitude
    """
    long, lat = lamber93_to_wgs84(coord_x, coord_y)

    # Check if the returned values are close to the expected values
    assert abs(long - expected_long) < 0.01, f"Expected {expected_long}, but got {long}"
    assert abs(lat - expected_lat) < 0.01, f"Expected {expected_lat}, but got {lat}"


@pytest.mark.parametrize(
    "address, expected_result, mock_response",
    [
        (
            "1 rue de la paix, Paris",
            [2.3317, 48.8693],
            {"features": [{"geometry": {"coordinates": [2.3317, 48.8693]}}]},
        ),
        ("10 Downing St, London", None, {"features": []}),  # Address in the UK
        (
            "1600 Pennsylvania Ave NW, Washington, DC",
            None,
            {"features": []},
        ),  # Address in the USA
        (
            "Eiffel Tower, Paris",
            [2.2945, 48.8584],
            {"features": [{"geometry": {"coordinates": [2.2945, 48.8584]}}]},
        ),
        (
            "Louvre Museum, Paris",
            [2.3364, 48.8606],
            {"features": [{"geometry": {"coordinates": [2.3364, 48.8606]}}]},
        ),
        ("Incorrect Address", None, {"features": []}),  # Address does not exist
    ],
)
def test_get_coordinates(mocker, address, expected_result, mock_response):
    """
    Test the get_coordinates function

    :param mocker: The pytest mocker fixture
    :param address: The address to get the coordinates from
    :param expected_result: The expected coordinates
    :param mock_response: The mock response from the requests.get function
    """
    mock_requests = mocker.patch("requests.get")
    mock_requests.return_value.json.return_value = mock_response

    assert get_coordinates(address) == (expected_result)


@pytest.mark.parametrize(
    "side_effect, call_count",
    [
        (
            requests.exceptions.RequestException("Error"),
            3,
        ),
    ],
)
def test_request_external_api_retry_fail(mocker, side_effect, call_count):
    """
    Test the get_coordinates function when a RequestException is raised and retried
    """
    mock_get = mocker.patch("requests.get")
    mock_get.side_effect = side_effect

    try:
        request_external_api("http://url")
    except requests.exceptions.RequestException:
        pass

    assert mock_get.call_count == call_count
