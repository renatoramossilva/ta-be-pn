"""Test data module"""

import pathlib

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from app.db import data


@pytest.fixture
def mock_df():
    """Mock dataframe"""
    return pd.DataFrame(
        {
            "Operateur": [20801, None, 20815, 20801],
            "x": [1000, 2000, None, 1000],
            "y": [4000, None, 6000, 4000],
            "2G": [1, 0, 1, 1],
            "3G": [1, 1, 0, 1],
            "4G": [1, 1, 1, 1],
        }
    )


@pytest.fixture
def mock_return_df():
    """Mock return dataframe"""
    return pd.DataFrame(
        {
            "Operateur": [20801.0],
            "x": [1000.0],
            "y": [4000.0],
            "2G": [1],
            "3G": [1],
            "4G": [1],
        }
    )


@pytest.fixture
def mock_csv_path(tmp_path):
    """Mock CSV file path"""
    csv_content = """Operateur;x;y;2G;3G;4G
        20801;1000;4000;1;1;1
        20810;2000;5000;0;1;1
        20815;3000;6000;1;0;1
    """
    csv_path = tmp_path / "mock_data.csv"
    csv_path.write_text(csv_content)
    return pathlib.Path(csv_path)


def test_validate_operator_data(
    mock_df, mock_return_df
):  # pylint: disable=redefined-outer-name
    """Test validate_operator_data function

    Tests scenarios:
    - Validate dataframe
    - Remove missing data
    - Remove duplicates
    """
    validated_df = data.validate_operator_data(mock_df)
    assert not validated_df.empty
    assert len(validated_df) == 1
    assert_frame_equal(validated_df, mock_return_df)


def test_load_csv_file(mocker, mock_csv_path):  # pylint: disable=redefined-outer-name
    """Test load_csv_file function

    Tests scenarios:
    - Load CSV file
    - Validate dataframe
    """
    mock_db_url = mocker.patch("app.db.data.DB_URL")
    mock_db_url.return_value.json.return_value = mock_csv_path

    df = data.load_csv_file(mock_csv_path)
    assert not df.empty
    assert len(df) == 3
    assert list(df.columns) == ["Operateur", "x", "y", "2G", "3G", "4G"]


def test_invalid_csv_file():
    """Test invalid CSV file"""
    with pytest.raises(FileNotFoundError, match="The file was not found"):
        data.load_csv_file(pathlib.Path("invalid_path.csv"))
