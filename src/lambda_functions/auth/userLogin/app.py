import os, json, boto3

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/initiate_auth.html

cognito = boto3.client('cognito-idp')
CLIENT_ID = os.environ['COGNITO_CLIENT_ID']

def lambda_handler(event, context):
    body = json.loads(event.get('body') or '{}')

    email = body.get('email')
    password = body.get('password')
    if not email or not password:
        return {
            'statusCode':400, 
            'body': json.dumps({'error':'email/password required'})
        }

    try:
        resp = cognito.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        auth_result = resp.get('AuthenticationResult', {})
        return {
            'statusCode':200, 
            'body': json.dumps({'auth': auth_result})
        }
    except Exception as e:
        return {
            'statusCode':401, 
            'body': json.dumps({'error': str(e)})
        }