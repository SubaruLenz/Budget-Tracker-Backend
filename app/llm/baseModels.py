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
