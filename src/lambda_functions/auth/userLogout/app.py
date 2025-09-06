import os, json, boto3

cognito = boto3.client("cognito-idp")
CLIENT_ID = os.environ["COGNITO_CLIENT_ID"]

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")

        access_token = body.get("access_token")
        if not access_token:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "access_token is required"})
            }

        cognito.global_sign_out(
            AccessToken=access_token
        )
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Successfully signed out"})
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }