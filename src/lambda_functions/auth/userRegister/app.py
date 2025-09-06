import os, json, boto3

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/sign_up.html

cognito = boto3.client('cognito-idp')
CLIENT_ID = os.environ['CLIENT_ID']

def lambda_handler(event, context):
    body = json.loads(event.get('body') or '{}')

    email = body.get('email')
    password = body.get('password')
    if not email or not password:
        return {
            'statusCode':400, 
            'body': json.dumps({'error':'email and password required'})
        }

    try:
        res = cognito.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
        )
        return {
            'statusCode':200, 
            'body': json.dumps({
                'message':'signup initiated', 
                'code_delivery': res.get('CodeDeliveryDetails')
            })
        }
    except cognito.exceptions.UsernameExistsException:
        return {
            'statusCode':409, 
            'body': json.dumps({'error':'user with email already exists'})
        }
    except Exception as e:
        return {
            'statusCode':500, 
            'body': json.dumps({'error': str(e)})
        }