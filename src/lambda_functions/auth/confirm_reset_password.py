import json
from src.utils.cognito import get_cognito_client, get_client_id

def lambda_handler(event, context):
    cognito = None

    try:
        body = json.loads(event.get("body", "{}"))

        email = body.get("email")
        code = body.get("code")
        new_password = body.get("new_password")
        if not email or not code or not new_password:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "success": False,
                    "error": "Missing email, code, or new_password"
                })
            }

        cognito = get_cognito_client()
        client_id = get_client_id() 
        cognito.confirm_forgot_password(
            cognitoId=client_id,
            Username=email,
            ConfirmationCode=code,
            Password=new_password
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "message": "Successfully reset password"
            })
        }

    except cognito.exceptions.CodeMismatchException:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "success": False,
                "error": "Invalid confirmation code"
            })
        }
    
    except cognito.exceptions.ExpiredCodeException:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "success": False,
                "error": "Confirmation code expired"
            })
        }
    
    except cognito.exceptions.InvalidPasswordException as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "success": False,
                "error": str(e)
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