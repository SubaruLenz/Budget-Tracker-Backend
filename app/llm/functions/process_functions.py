#Libraries
import boto3, logging, os, json
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

#Dependencies
from app.config.log_config import setup_config
from app.llm.models.response_models import TransactionModel
from app.llm.functions.resource_functions import get_transaction_types, get_current_time

#Logging
setup_config()
logger = logging.getLogger(__name__)

# Load .env file
load_dotenv()

# Get the database URL
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
MODEL_ID = os.getenv('MODEL_ID')

# Check if AWS credentials are set
if AWS_ACCESS_KEY_ID is None or AWS_SECRET_ACCESS_KEY is None or AWS_REGION is None:
    raise ValueError("Missing AWS related in environment variables")

bedrock = boto3.client(
    'bedrock-runtime',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

#Extract transaction to JSON format
async def process_transaction(input: str, db: Session):
    transaction_types = get_transaction_types(db)
    current_time = get_current_time()

    prompt = f"""Extract transaction info from "{input}"
    Instruction: 
    - Return only valid JSON with: name (string), amount (float), date (YY-MM-DD HH:MM:SS), transaction_type_id (integer)
    - If the input is unclear please response with "", 0.0, 1 depends on the variable
    - Response with positive amount for income and minus amount for expenses
    Input example: {{"I spent 5 dollar while hanging out with friends yesterday"}}
    Response example: {{"name": "Hang out with friend", "amount": -5.0, "date": "2025-08-05 00:00:00"}}
    Resources:
    - Current time: {current_time}
    - Transaction type (including type id and type name): {transaction_types}
    """

    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"temperature": 0.1}
    )
    
    raw_result = response['output']['message']['content'][0]['text']
    json_data = json.loads(raw_result)
    return TransactionModel(**json_data)

#Analyse budget
async def process_analysis(input: str, db: Session):
    analysis_prompt = f"""Analyze expenses based on: "{input}"
    Provide a brief expense analysis summary.
    """
    
    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": analysis_prompt}]}],
        inferenceConfig={"temperature": 0.3}
    )
    
    return response['output']['message']['content'][0]['text']