from pydantic import BaseModel
import datetime

class TransactionTypeModel(BaseModel):
    id: int
    name: str = "Unknown"

class TransactionModel(BaseModel):
    name: str = ""
    amount: float = 0.0
    date: str = datetime.datetime.now().strftime("%Y-%m-%d")
    transaction_type_id: int = 1