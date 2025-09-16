import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_db(mocker):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    # context manager support for 'with cursor as cur:'
    mock_cursor.__enter__.return_value = mock_cursor
    mock_cursor.__exit__.return_value = False

    mocker.patch("src.utils.db.get_cursor", return_value=(mock_conn, mock_cursor))
    return mock_conn, mock_cursor

@pytest.fixture
def mock_cognito(mocker):
    mock_client = MagicMock()
    mocker.patch("src.utils.cognito.get_cognito_client", return_value=mock_client)
    mocker.patch(
        "src.utils.cognito.get_client_id",
        return_value="fake-client-id"
    )
    return mock_client