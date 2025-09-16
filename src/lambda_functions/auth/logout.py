import json
from src.utils.cognito import get_cognito_client

def lambda_handler(event, context):
    cognito = None

    try:
        body = json.loads(event.get("body") or "{}")

        access_token = body.get("access_token")
        if not access_token:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "success": False,
                    "error": "Missing access_token"
                })
            }

        cognito = get_cognito_client()
        cognito.global_sign_out(
            AccessToken=access_token
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "message": "Successfully signed out"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "message": "Internal server error"
            })
        }