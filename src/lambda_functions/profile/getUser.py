import json
from utils.db import get_cursor

def lambda_handler(event, context):
    try:
        # Extract user email from Cognito claims
        claims = event["requestContext"]["authorizer"]["claims"]
        email = claims.get("email")
        if not email:
            return {
                "statusCode": 403,
                "body": json.dumps({
                    "success": False,
                    "error": "Unauthorized"
                })
            }

        conn, cursor = get_cursor()
        with cursor as cur:
            cur.execute("SELECT * FROM Users WHERE email = %s;", (email,))
            user = cur.fetchone()

        if not user:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "success": False,
                    "error": "User data not found"
                })
            }

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True, 
                "data": user
            }, default=str)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "message": "Internal server error"
            })
        }