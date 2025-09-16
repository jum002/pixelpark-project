import json

def test_get_profile_success(mock_db):
    from src.lambda_functions.profile.getUser import lambda_handler as get_profile_handler

    mock_conn, mock_cursor = mock_db
    mock_data = {"email": "test@example.com", "name": "Test User"}
    mock_cursor.fetchone.return_value = mock_data

    event = {
        "requestContext": {
            "authorizer": {
                "claims": {"email": "test@example.com"}
            }
        }
    }
    result = get_profile_handler(event, None)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["success"] is True
    assert body["data"] == mock_data


def test_get_profile_unauthorized(mock_db):
    from src.lambda_functions.profile.getUser import lambda_handler as get_profile_handler
    
    event = {
        "requestContext": {
            "authorizer": {"claims": {}}
        }
    }
    result = get_profile_handler(event, None)

    assert result["statusCode"] == 403
    body = json.loads(result["body"])
    assert body["error"] == "Unauthorized"