import boto3
import json
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Load .env file
load_dotenv()

#Get all secrets from secret manager
def get_secret(secret_name: str, region_name: str = "us-east-1"):
    client = boto3.client(
        'secretsmanager',
        region_name=region_name,
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except ClientError as e:
        raise ValueError(f"Raising error{e}")

def get_all_config():
    secret_name = os.getenv("SECRET_NAME")
    region = os.getenv("AWS_REGION")
    
    if secret_name is None or region is None:
        raise ValueError("Please input secret name and region")

    try:
        return get_secret(secret_name, region)
    except Exception as e:
        raise ValueError(f"Could not retrieve secrets: {e}")