import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Export configuration values from .env
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRATION = os.getenv('ACCESS_TOKEN_EXPIRATION', '480')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
MODEL_ID = os.getenv('MODEL_ID')