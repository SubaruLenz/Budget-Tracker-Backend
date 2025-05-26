from google import genai
from dotenv import load_dotenv
#from .baseModels import Transaction
import os

from pydantic import BaseModel
import enum, datetime

class TransactionType(enum.Enum):
    FOOD="food"
    COMMUTE="commute"
    OTHER="other"

class Transaction(BaseModel):
    name: str
    ammount: int
    date: datetime.datetime
    transaction_type: TransactionType


load_dotenv()

AI_API = os.getenv("AI_API")
if not AI_API:
    raise ValueError("AI_API environment variable is not set. Please check your .env file.")

client = genai.Client(api_key=AI_API)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="I spent 20$ for food yesterday",
    config={
        "response_mime_type": "application/json",
        "response_schema": Transaction,
    },
)

print(response.text)
