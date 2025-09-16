import json
from utils.cognito import get_cognito_client, get_client_id

def lambda_handler(event, context):
    cognito = None

    try:
        body = json.loads(event.get("body") or "{}")

        email = body.get("email")
        if not email:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "success": False,
                    "error": "Missing email"
                })
            }

        cognito = get_cognito_client()
        client_id = get_client_id() 
        resp = cognito.resend_confirmation_code(
            ClientId=client_id,
            Username=email
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "message": "Successfully resent confirmation code",
            })
        }

    except cognito.exceptions.UserNotFoundException:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "success": False,
                "error": "User not found"
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