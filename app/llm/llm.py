#Libraries
import boto3, logging, os, json
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

#Dependencies
from app.config.log_config import setup_config
from app.llm.functions.process_functions import process_transaction, process_analysis

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

#Functions


#Process
bedrock = boto3.client(
    'bedrock-runtime',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

async def detect_intent(input: str):
    intent_prompt = f"""Classify the intent of: "{input}"
    Return only one word:
    - "transaction" for recording expenses/income
    - "analysis" for analyzing/reviewing expenses
    """
    
    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": intent_prompt}]}],
        inferenceConfig={"temperature": 0.1}
    )
    
    return response['output']['message']['content'][0]['text'].strip().lower()

async def llm_process(input: str, db: Session):
    try:
        intent = await detect_intent(input)
        logger.info(f"Detected intent: {intent}")
        
        if intent == "transaction":
            result = await process_transaction(input, db)
            logger.info(f"Transaction result: {result}")
            return f"Transaction processed: {result.name} - ${result.amount}"
        elif intent == "analysis":
            result = await process_analysis(input, db)
            logger.info(f"Analysis result: {result}")
            return result
        else:
            # Default to transaction
            result = await process_transaction(input, db)
            return f"Transaction processed: {result.name} - ${result.amount}"
        
    except Exception as e:
        logger.error(f"Error processing LLM request: {str(e)}")
        return f"Sorry, I couldn't process your request: {str(e)}"
