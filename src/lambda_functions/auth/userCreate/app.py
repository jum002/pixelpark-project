import os
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


def lambda_handler(event, context):
    """
    This Lambda is triggered after a user confirms signup in Cognito.
    The event contains the user attributes from Cognito.
    """
    try:
        user_attrs = event["userAttributes"]
        email = user_attrs.get("email")

        if not email:
            raise ValueError("Missing required user email.")

        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (email)
                VALUES (%s)
                ON CONFLICT (email) DO NOTHING;
                """,
                (email)
            )
        conn.commit()

        return event

    except Exception as e:
        print("Error inserting user into DB:", str(e))
        return event