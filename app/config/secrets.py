import boto3
import json
import os
from botocore.exceptions import ClientError

def get_secret(secret_name: str, region_name: str = "us-east-1"):
    """Retrieve secret from AWS Secrets Manager"""
    client = boto3.client(
        'secretsmanager',
        region_name=region_name
    )
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except ClientError as e:
        raise e

def get_all_config():
    """Get all configuration from secrets manager or environment"""
    # For local development, use environment variables
    if os.getenv("DATABASE_URL"):
        return {
            'DATABASE_URL': os.getenv("DATABASE_URL"),
            'SECRET_KEY': os.getenv("SECRET_KEY"),
            'ALGORITHM': os.getenv("ALGORITHM"),
            'ACCESS_TOKEN_EXPIRATION': os.getenv("ACCESS_TOKEN_EXPIRATION"),
            'AWS_ACCESS_KEY_ID': os.getenv("AWS_ACCESS_KEY_ID"),
            'AWS_SECRET_ACCESS_KEY': os.getenv("AWS_SECRET_ACCESS_KEY"),
            'AWS_REGION': os.getenv("AWS_REGION"),
            'MODEL_ID': os.getenv("MODEL_ID")
        }
    
    # For production, get everything from secrets manager
    secret_name = os.getenv("SECRET_NAME", "budget-tracker/all-secrets")
    region = os.getenv("AWS_REGION", "us-east-1")
    
    try:
        return get_secret(secret_name, region)
    except Exception as e:
        raise ValueError(f"Could not retrieve secrets: {e}")

def get_database_url():
    """Get database URL"""
    config = get_all_config()
    return config.get('DATABASE_URL')