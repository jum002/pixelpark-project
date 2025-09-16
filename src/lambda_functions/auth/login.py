import json, textwrap
from utils.db import get_conn
from utils.cognito import get_cognito_client, get_client_id

def lambda_handler(event, context):
    conn = None
    cognito = None

    try: 
        body = json.loads(event.get('body') or '{}')

        email = body.get('email')
        password = body.get('password')
        if not email or not password:
            return {
                "statusCode": 400, 
                "body": json.dumps({
                    "success": False,
                    "error": "Missing email or password"
                })
            }

        cognito = get_cognito_client()
        client_id = get_client_id() 
        resp = cognito.initiate_auth(
            ClientId=client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password
            }
        ).get("AuthenticationResult", {})

        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute(
                textwrap.dedent("""
                    INSERT INTO users (email, status)
                    VALUES (%s, 'active')
                    ON CONFLICT (email) DO UPDATE SET status = 'active';
                """),
                (email,)
            )
        conn.commit()

        return {
            "statusCode": 200, 
            "body": json.dumps({"auth": resp})
        }

    except cognito.exceptions.UserNotFoundException:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "success": False,
                "error": "User not found"
            })
        }
    
    except cognito.exceptions.NotAuthorizedException:
        return {
            "statusCode": 401,
            "body": json.dumps({
                "success": False,
                "error": "Incorrect username or password"
            })
        }
    
    except cognito.exceptions.UserNotConfirmedException:
        return {
            "statusCode": 403,
            "body": json.dumps({
                "success": False,
                "error": "User not confirmed"
            })
        }
    
    except Exception as e:
        if conn and not conn.closed:
            conn.rollback()

        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "message": "Internal server error"
            })
        }