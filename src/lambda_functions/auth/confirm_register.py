import json, textwrap
from utils.db import get_conn
from utils.cognito import get_cognito_client, get_client_id

def lambda_handler(event, context):
    conn = None

    try:
        body = json.loads(event.get("body") or "{}")

        email = body.get("email")
        code = body.get("code")
        if not email or not code:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "success": False,
                    "error": "Missing email or code"
                })
            }
    
        cognito = get_cognito_client()
        client_id = get_client_id() 
        cognito.confirm_sign_up(
            ClientId=client_id,
            Username=email,
            ConfirmationCode=code
        )

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
            "body": json.dumps({
                "success": True,
                "message": "Successfully completed sign up"
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