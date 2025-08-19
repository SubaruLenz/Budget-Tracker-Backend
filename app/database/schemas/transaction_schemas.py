from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime

class Transactions(BaseModel):
    name: str
    amount: Decimal
    transaction_type_id: int
    model_config = ConfigDict(from_attributes=True)

class ResponseTransactions(Transactions):
    id: int
    transaction_date: datetime
    wallet_id: int

class CreateTransaction(BaseModel):
    name: str
    amount: Decimal
    transaction_type_id: int
    wallet_id: int

class TransactionCategory(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class CreateTransactionCategory(BaseModel):
    name: str

class TransactionType(BaseModel):
    id: int
    name: str
    category_id: int
    model_config = ConfigDict(from_attributes=True)