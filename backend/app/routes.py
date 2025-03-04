"""
This module contains the FastAPI routes for the mobile network coverage API.
"""

# pylint: disable=import-error

import time

from fastapi import APIRouter, HTTPException  # type: ignore
from prometheus_client import Counter, Gauge, Histogram

from app.db.data import find_network_coverage
from app.utils.common import get_coordinates
from app.utils.logger import setup_logger

router = APIRouter()

LOG = setup_logger(__name__)


PROMETHEUS_REQUEST_COUNT = Counter(
    "ta_be_pn_metrics_request_count", "requests count to /coverage"
)

PROMETHEUS_REQUEST_LATENCY = Histogram(
    "ta_be_pn_metrics_request_latency_seconds", "Request latency to /coverage"
)

PROMETHEUS_IN_PROGRESS = Gauge(
    "ta_be_pn_metrics_in_progress", "Number of requests in progress to /coverage"
)

PROMETHEUS_REQUEST_FAILURES = Counter(
    "ta_be_pn_metrics_request_failures", "Number of failed requests to /coverage"
)


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
    PROMETHEUS_REQUEST_COUNT.inc()
    PROMETHEUS_IN_PROGRESS.inc()
    start_time = time.time()

    data_coverage = {}

    try:
        LOG.info("Getting network coverage for address %s: address")
        coordinates = get_coordinates(address)

        if coordinates is None:
            LOG.error("Unable to get coordinates for the given address")
            raise HTTPException(
                status_code=400,
                detail="Unable to get coordinates for the given address",
            )

        data_coverage = find_network_coverage(*coordinates)

        if not data_coverage:
            LOG.error("Unable to find network coverage for the given location")
            raise HTTPException(
                status_code=400,
                detail="Unable to find network coverage for the given location",
            )
    except Exception as ex:  # pylint: disable=broad-except
        LOG.error("An error occurred while fetching network coverage: %s", ex)
        PROMETHEUS_REQUEST_FAILURES.inc()
        raise HTTPException(
            400, "Unable to get coordinates for the given address"
        ) from ex

    latency = time.time() - start_time
    PROMETHEUS_REQUEST_LATENCY.observe(latency)
    PROMETHEUS_IN_PROGRESS.dec()

    return data_coverage
