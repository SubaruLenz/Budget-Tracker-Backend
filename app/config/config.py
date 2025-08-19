from .secrets import get_all_config

# Load all configuration
config = get_all_config()

# Export commonly used values
DATABASE_URL = config.get('DATABASE_URL')
SECRET_KEY = config.get('SECRET_KEY')
ALGORITHM = config.get('ALGORITHM')
ACCESS_TOKEN_EXPIRATION = int(config.get('ACCESS_TOKEN_EXPIRATION') or 480)
AWS_ACCESS_KEY_ID = config.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = config.get('AWS_REGION')
MODEL_ID = config.get('MODEL_ID')