from pydantic import BaseModel
from datetime import datetime
class Users(BaseModel):
    id: int
    username: str
    email: str
    password: str
    created_date: datetime

    class Config:
        orm_mode = True

class Wallets(BaseModel):
    id: int
    name: str
    user_id: int
    balance: float
    created_date: datetime

    class Config:
        orm_mode = True

class Transactions(BaseModel):
    id: int
    user_id: int
    amount: float
    transaction_type: str
    category: str
    created_date: datetime

    class Config:
        orm_mode = True

class Conversations(BaseModel):
    id: int
    user_id: int
    amount: float
    transaction_type: str
    category: str
    date: datetime

    class Config:
        orm_mode = True

class Chats(BaseModel):
    id: int
    user_id: int
    message: str
    timestamp: datetime

    class Config:
        orm_mode = True

    