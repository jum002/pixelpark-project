import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor

_conn = None

def get_conn():
    global _conn
    if _conn is None or _conn.closed:
        _conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            port=5432,
        )
    return _conn

def lambda_handler(event, context):
    try:        
        product_id = event["pathParameters"]["id"]

        conn = get_conn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f"SELECT * FROM Products WHERE id = {product_id};")
            rows = cur.fetchall()
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "data": rows
            }, default=str)
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "message": str(e)
            }, default=str)
        }
