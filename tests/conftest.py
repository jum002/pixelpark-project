import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_db(mocker):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    # context manager support
    mock_cursor.__enter__.return_value = mock_cursor
    mock_cursor.__exit__.return_value = False

    modules = [
        "lambda_functions.products.getAll",
        "lambda_functions.products.getById",
        "lambda_functions.profile.getUser",
        "lambda_functions.auth.register",
        "lambda_functions.auth.confirm_register",
        "lambda_functions.auth.login",
    ]

    for module in modules:
        mocker.patch(f"{module}.get_cursor", return_value=(mock_conn, mock_cursor))

    return mock_conn, mock_cursor


@pytest.fixture
def mock_cognito(mocker):
    mock_client = MagicMock()

    modules = [
        "lambda_functions.auth.register",
        "lambda_functions.auth.confirm_register",
        "lambda_functions.auth.resend_confirmation",
        "lambda_functions.auth.forgot_password",
        "lambda_functions.auth.confirm_reset_password",
        "lambda_functions.auth.login",
        "lambda_functions.auth.logout"
    ]

    for module in modules:
        mocker.patch(f"{module}.get_cognito_client", return_value=mock_client)
        mocker.patch(f"{module}.get_client_id", return_value="mock-client-id")

    return mock_client