import os, json, boto3

cognito = boto3.client('cognito-idp')
CLIENT_ID = os.environ['CLIENT_ID']

def lambda_handler(event, context):
    body = json.loads(event.get('body') or '{}')

    email = body.get('email')
    code = body.get('code')
    if not email or not code:
        return {
            'statusCode':400, 
            'body': json.dumps({'error':'email and code required'})
        }

    try:
        cognito.confirm_sign_up(ClientId=CLIENT_ID, Username=email, ConfirmationCode=code)
        return {
            'statusCode':200, 
            'body': json.dumps({'message':'confirmed'})
        }
    except Exception as e:
        return {
            'statusCode':400, 
            'body': json.dumps({'error': str(e)})
        }