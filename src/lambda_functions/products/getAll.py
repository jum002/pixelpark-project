import json
from utils.db import get_cursor

def lambda_handler(event, context):
    try:        
        conn, cursor = get_cursor()
        with cursor as cur:
            cur.execute("SELECT * FROM Products;")
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
                "message": "Internal server error"
            })
        }
