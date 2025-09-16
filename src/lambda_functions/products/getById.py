import json
from utils.db import get_cursor

def lambda_handler(event, context):
    try:        
        product_id = event["pathParameters"]["id"]

        conn, cursor = get_cursor()
        with cursor as cur:
            cur.execute("SELECT * FROM Products WHERE id = %s;", (product_id,))
            row = cur.fetchone()

        if not row:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "success": False,
                    "error": "Product data not found"
                })
            }
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "data": row
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
