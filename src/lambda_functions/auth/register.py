import json, textwrap
from src.utils.db import get_cursor
from src.utils.cognito import get_cognito_client, get_client_id

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
        res = cognito.sign_up(
            ClientId=client_id,
            Username=email,
            Password=password,
        )

        conn, cursor = get_cursor()
        with cursor as cur:
            cur.execute(
                textwrap.dedent("""
                    INSERT INTO users (email, status)
                    VALUES (%s, 'pending')
                    ON CONFLICT (email) DO UPDATE SET status = 'pending';
                """),
                (email,)
            )
        conn.commit()

        return {
            "statusCode":200, 
            "body": json.dumps({
                "success": True,
                "message": "Signup initiated", 
                "code_delivery": res.get("CodeDeliveryDetails")
            })
        }
    
    except cognito.exceptions.UsernameExistsException:
        return {
            "statusCode": 409,
            "body": json.dumps({
                "success": False,
                "error": "User with email already exists"
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