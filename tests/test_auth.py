import json, textwrap
from botocore.exceptions import ClientError

from lambda_functions.auth.register import lambda_handler as register_handler
from lambda_functions.auth.confirm_register import lambda_handler as confirm_registration_handler
from lambda_functions.auth.resend_confirmation import lambda_handler as resend_confirmation_handler
from lambda_functions.auth.forgot_password import lambda_handler as forgot_password_handler
from lambda_functions.auth.confirm_reset_password import lambda_handler as confirm_reset_handler
from lambda_functions.auth.login import lambda_handler as login_handler
from lambda_functions.auth.logout import lambda_handler as logout_handler


"""
Register
"""

def test_register_success(mock_db, mock_cognito):
    mock_resp = {
        "CodeDeliveryDetails": {"Destination": "test@example.com", "DeliveryMedium": "EMAIL"}
    }
    mock_cognito.sign_up.return_value = mock_resp

    event = {"body": json.dumps({"email": "test@example.com", "password": "Secret@123456"})}
    result = register_handler(event, None)

    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert body["success"] is True
    assert body["message"] == "Signup initiated"
    assert body["code_delivery"] == mock_resp["CodeDeliveryDetails"]

    mock_cognito.sign_up.assert_called_once_with(
        ClientId="mock-client-id",
        Username="test@example.com",
        Password="Secret@123456"
    )

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


"""
Confirm Register
"""

def test_confirm_register_success(mock_db, mock_cognito):
    event = {"body": json.dumps({"email": "test@example.com", "code": "123456"})}
    result = confirm_registration_handler(event, {}) 

    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert body["success"] is True
    assert body["message"] == "Successfully completed sign up"

    mock_cognito.confirm_sign_up.assert_called_once_with(
        ClientId="mock-client-id",
        Username="test@example.com",
        ConfirmationCode="123456"
    )

    mock_conn, mock_cursor = mock_db
    mock_cursor.execute.assert_called_once_with(
        textwrap.dedent("""
            INSERT INTO users (email, status)
            VALUES (%s, 'active')
            ON CONFLICT (email) DO UPDATE SET status = 'active';
        """),
        ("test@example.com",)
    )
    mock_conn.commit.assert_called_once()


def test_confirm_register_missing_code():
    event = {"body": json.dumps({"email": "test@example.com"})}
    result = confirm_registration_handler(event, {})

    body = json.loads(result["body"])
    assert result["statusCode"] == 400
    assert body["success"] is False
    assert body["error"] == "Missing email or code"


"""
Resend Confirmation
"""

def test_resend_confirmation_success(mock_db, mock_cognito):
    event = {
        "body": json.dumps({"email": "test@example.com"})
    }
    result = resend_confirmation_handler(event, None)

    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert body["success"] is True
    assert body["message"] == "Successfully resent confirmation code"

    mock_cognito.resend_confirmation_code.assert_called_once_with(
        ClientId="mock-client-id",
        Username="test@example.com"
    )


def test_resend_confirmation_missing_email(mock_db, mock_cognito):
    event = {"body": json.dumps({})}
    result = resend_confirmation_handler(event, None)

    body = json.loads(result["body"])
    assert result["statusCode"] == 400
    assert body["success"] is False
    assert body["error"] == "Missing email"


def test_resend_confirmation_user_not_found(mock_db, mock_cognito):
    mock_cognito.resend_confirmation_code.side_effect = ClientError(
        {"Error": {"Code": "UserNotFoundException", "Message": "User not found"}},
        "resend_confirmation_code"
    )

    event = {"body": json.dumps({"email": "missing@example.com"})}
    response = resend_confirmation_handler(event, None)

    body = json.loads(response["body"])
    assert response["statusCode"] == 404
    assert body["success"] is False
    assert body["error"] == "User not found"


"""
Forgot Password
"""

def test_forgot_password_success(mock_db, mock_cognito):
    event = {
        "body": json.dumps({"email": "test@example.com"})
    }
    result = forgot_password_handler(event, None)

    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert body["success"] is True
    assert body["message"] == "Successfully sent password reset code"

    mock_cognito.forgot_password.assert_called_once_with(
        ClientId="mock-client-id",
        Username="test@example.com"
    )


"""
Confirm Reset Password
"""

def test_confirm_reset_password_success(mock_db, mock_cognito):
    event = {
        "body": json.dumps({
            "email": "test@example.com",
            "code": "123456",
            "new_password": "NewSecret@123"
        })
    }
    result = confirm_reset_handler(event, None)

    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert body["success"] is True
    assert body["message"] == "Successfully reset password"

    mock_cognito.confirm_forgot_password.assert_called_once_with(
        ClientId="mock-client-id",
        Username="test@example.com",
        ConfirmationCode="123456",
        Password="NewSecret@123"
    )


"""
Login
"""

def test_login_success(mock_db, mock_cognito):
    event = {
        "body": json.dumps({
            "email": "test@example.com",
            "password": "Secret@123"
        })
    }
    mock_cognito.initiate_auth.return_value = {"AuthenticationResult": {"AccessToken": "mock-token"}}

    result = login_handler(event, None)

    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert body["auth"] == {"AccessToken": "mock-token"}

    mock_cognito.initiate_auth.assert_called_once_with(
        ClientId="mock-client-id",
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": "test@example.com",
            "PASSWORD": "Secret@123"
        }
    )


def test_login_user_not_found(mock_db, mock_cognito):
    event = {
        "body": json.dumps({
            "email": "missing@example.com",
            "password": "Secret@123"
        })
    }
    mock_cognito.initiate_auth.side_effect = ClientError(
        {"Error": {"Code": "UserNotFoundException", "Message": "User not found"}},
        "initiate_auth"
    )

    result = login_handler(event, None)

    body = json.loads(result["body"])
    assert result["statusCode"] == 404
    assert body["success"] is False
    assert body["error"] == "User not found"


"""
Logout
"""

def test_logout_success(mock_cognito):
    event = {
        "body": json.dumps({"access_token": "mock-access-token"})
    }

    result = logout_handler(event, None)

    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert body["success"] is True
    assert body["message"] == "Successfully signed out"

    mock_cognito.global_sign_out.assert_called_once_with(
        AccessToken="mock-access-token"
    )