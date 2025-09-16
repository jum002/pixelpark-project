import boto3
import os

def get_cognito_client():
    return boto3.client("cognito-idp")

def get_client_id():
    return os.environ["COGNITO_CLIENT_ID"]