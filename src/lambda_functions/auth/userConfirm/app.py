import os, json, boto3
import psycopg2

_conn = None

def get_conn():
    global _conn
    if _conn is None or _conn.closed:
        _conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            port=5432
        )
    return _conn

cognito = boto3.client('cognito-idp')
CLIENT_ID = os.environ['COGNITO_CLIENT_ID']

def lambda_handler(event, context):
    body = json.loads(event.get("body") or "{}")

    email = body.get("email")
    code = body.get("code")
    if not email or not code:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "email and code required"})
        }

    try:
        cognito.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            ConfirmationCode=code
        )

        # TODO: ensure atomicity
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (email)
                VALUES (%s)
                ON CONFLICT (email) DO NOTHING;
                """,
                (email,)
            )
        conn.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "message": "successfully completed sign up"
            })
        }

    except Exception as e:
        # rollback DB transaction if open
        if _conn and not _conn.closed:
            _conn.rollback()
        return {
            "statusCode": 400,
            "body": json.dumps({
                "success": False,
                "error": str(e)
            })
        }