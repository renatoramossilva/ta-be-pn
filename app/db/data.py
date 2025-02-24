"""Data module to handle the network coverage data"""

import pathlib

import numpy as np
import pandas as pd

from app.utils.common import wgs84_to_lamber93
from app.utils.logger import setup_logger

DB_URL: str = pathlib.Path(
    "app/db/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv"
)
LOG = setup_logger(__name__)


# Operators
OPERATORS = {
    20801: "Orange",
    20803: "MobiquiThings",
    20804: "NetGroup",
    20805: "Globalstar Europe",
    20808: "Completel",
    20810: "SFR",
    20815: "Free",
    20820: "Bouygues",
}


def validate_operator_data(df):
    """
    Validate dataframes

    This function validates the data in the dataframe by converting
    the columns to numeric and removing rows with missing data
    and duplicates.

    **Request Body:**
    - `df`: Dataframe to validate

    **Returns:**
    A valid dataframe
    """
    LOG.info("Validating operator data")

    # List of columns to validate
    columns = ["Operateur", "x", "y", "2G", "3G", "4G" ""]

    # Convert columns to numeric, if the values are not numeric,
    # they will be converted to NaN
    LOG.info("Converting columns to numeric")
    for column in columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    LOG.info("Removing rows with missing data")
    df = df.dropna(subset=columns)  # Remove rows with missing data

    LOG.info("Removing duplicate rows")
    df = df.drop_duplicates()  # Remove duplicate rows

    LOG.info("Operator data validated")

    return df


def load_csv_file(csv_path: pathlib.Path) -> pd.DataFrame:
    """
    Load a CSV file

    **Request Body:**
    - `csv_path`: Path to the CSV file

    **Returns:**
    A pandas DataFrame with the CSV data
    """
    LOG.info("Loading CSV file")
    if csv_path.exists():
        df = pd.read_csv(csv_path, delimiter=";")
        df = validate_operator_data(df)
    else:
        LOG.error("The file was not found: %s", csv_path)
        return {}

    return df


def find_network_coverage(long: float, lat: float) -> dict[str, dict[str, bool]]:
    """
    Find the network coverage for a given location

    **Request Body:**
    - `lat`: Latitude of the location
    - `long`: Longitude of the location

    **Returns:**
    A dictionary containing the list of operators and their coverage
        for the given location

        e.g.
        {
            "Orange": {
                "2G": True,
                "3G": True,
                "4G": True
            },
            "SFR": {
                "2G": False,
                "3G": True,
                "4G": True
            },
            ...
        }
    """
    LOG.info("Finding network coverage for location: %s(lat), %s(long)", lat, long)

    # Convert WGS84 to Lambert93
    x_target, y_target = wgs84_to_lamber93(lat, long)

    df = load_csv_file(DB_URL)

    # Convert columns to integers
    df["x"] = df["x"].astype("Int64")
    df["y"] = df["y"].astype("Int64")

    # Calculate euclidean distance
    LOG.info("Calculating euclidean distance")
    df["distance"] = np.sqrt(
        (df["x"] - int(x_target)) ** 2 + (df["y"] - int(y_target)) ** 2
    )

    df["distance"] = df["distance"].astype("Int64")
    distance_threshold = 100  # Threshold distance in meters

    LOG.info("Filtering nearby operators")
    nearby_operators = df[
        df["distance"] <= distance_threshold
    ]  # Filter nearby operators

    coverage_data = {}

    # Get coverage data for each operator
    LOG.info("Getting coverage data for nearby operators")
    for _, row in nearby_operators.iterrows():
        operator_name = OPERATORS.get(int(row["Operateur"]), "Unknown")
        coverage_data[operator_name] = {
            "2G": bool(row["2G"]),
            "3G": bool(row["3G"]),
            "4G": bool(row["4G"]),
        }

    return coverage_data
