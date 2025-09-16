import json, textwrap

from src.lambda_functions.auth.confirm_register import lambda_handler as confirm_handler
from src.lambda_functions.auth.login import lambda_handler as login_handler

def test_register_success(mock_db, mock_cognito):
    from src.lambda_functions.auth.register import lambda_handler as register_handler

    mock_resp = {
        "CodeDeliveryDetails": {"Destination": "test@example.com", "DeliveryMedium": "EMAIL"}
    }
    mock_cognito.sign_up.return_value = mock_resp

    event = {"body": json.dumps({"email": "test@example.com", "password": "Secret@123456"})}
    result = register_handler(event, None)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["success"] is True
    assert body["message"] == "Signup initiated"
    assert body["code_delivery"] == mock_resp["CodeDeliveryDetails"]
    mock_cognito.sign_up.assert_called_once()

    mock_conn, mock_cursor = mock_db
    mock_cursor.execute.assert_called_once_with(
        textwrap.dedent("""
            INSERT INTO users (email, status)
            VALUES (%s, 'pending')
            ON CONFLICT (email) DO UPDATE SET status = 'pending';
        """),
        ("test@example.com",)
    )
    mock_conn.commit.assert_called_once()


def test_confirm_register_success():
    pass

def test_confirm_resend():
    pass

def test_forgot_password_success():
    pass

def test_confirm_reset_password_success():
    pass

def test_login_success():
    pass

def test_logout_success():
    pass