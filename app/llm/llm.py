#Libraries
import boto3, logging, os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

#Dependencies
from app.config.log_config import setup_config
from app.llm.functions.llm_functions import get_transaction_types, get_current_time

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

async def llm_process(input: str, db: Session):
    try:
        #Get Resources
        transaction_types = get_transaction_types(db)
        current_time = get_current_time()

        #Prompt
        promt = f"""Extract transaction info from "{input}"
        Instruction: Return only valid JSON with: name (string), amount (float), date (YY-MM-DD HH:MM:SS), transaction_type_id (integer)
        Input example: {{"I spent 5 dollar while hanging out with friends yesterday"}}
        Response example: {{"name": "Hang out with friend", "amount": -5.0, "date":}}
        Resources:
        - Current time: {current_time}
        - Transaction type (including type id and type name): {transaction_types}
        """

        response = bedrock.converse(
            modelId=MODEL_ID,
            messages=[
                {"role": "user", "content": [{"text": promt}]}
            ]
        )
        
        # Extract response text
        result = response['output']['message']['content'][0]['text']
        logger.info(f"LLM Response: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error processing LLM request: {str(e)}")
        raise
