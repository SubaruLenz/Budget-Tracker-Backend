from pydantic import BaseModel
import enum, datetime

class TransactionModel(BaseModel):
    id: int
    name: str = "Unknown"