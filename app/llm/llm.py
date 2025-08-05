#Libraries
import boto3, logging, os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

#Dependencies
from app.config.log_config import setup_config
from app.llm.functions.get_transaction_types_function import get_transaction_types

#Logging
setup_config()
logger = logging.getLogger(__name__)

# Load .env file
load_dotenv()

# Get the database URL
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION =os.getenv('AWS_REGION')

# Check if DATABASE_URL is set
if AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY or AWS_REGION is None:
    raise ValueError("Missing AWS related in environment variables")

#Functions


#Process
bedrock = boto3.client(
    'bedrock-runtime',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

def 

async def process(input: str, db: Session):
    try:
        transaction_types = get_transaction_types(db)
        promt = f"""
        """