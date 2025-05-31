from pydantic import BaseModel, EmailStr
from datetime import datetime

class Users(BaseModel):
    username: str
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserInDB(Users):
    hashed_password: str

#Optional
class responseUsers(Users):
    id: int
    create_date: datetime

class Wallets(BaseModel):
    name: str
    user_id: int
    balance: float

    class Config:
        from_attributes = True

#Optional
class responseWallets(Wallets):
    id: int
    created_date: datetime


class Transactions(BaseModel):
    user_id: int
    amount: float
    transaction_type: str
    category: str

    class Config:
        from_attributes = True

class responseTransactions(Transactions):
    id: int
    created_date: datetime


class Conversations(BaseModel):
    id: int
    user_id: int
    amount: float
    transaction_type: str
    category: str
    date: datetime

    class Config:
        from_attributes = True

class Chats(BaseModel):
    id: int
    user_id: int
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = ""