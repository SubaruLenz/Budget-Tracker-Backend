from pydantic import BaseModel, EmailStr, ConfigDict
from decimal import Decimal
from datetime import datetime

#User
class Users(BaseModel):
    id: int = 1
    username: str = "johndoe"
    name: str = "John Doe"
    email: EmailStr = "john@example.com"

    model_config = ConfigDict(from_attributes=True)

class UserInDB(Users):
    hashed_password: str = "hashed_password"

class CreateUser(BaseModel):
    username: str = "johndoe"
    name: str = "John Doe"
    email: EmailStr = "john@example.com"
    hashed_password: str = "hashed_password"

    model_config = ConfigDict(from_attributes=True)

class UpdateUser(BaseModel):
    name: str = "John Doe"
    email: EmailStr = "john@example.com"
    hashed_password: str = "hashed_password"

    model_config = ConfigDict(from_attributes=True)

#Wallets
class Wallets(BaseModel):
    name: str
    balance: Decimal = Decimal(0.00)

    model_config = ConfigDict(from_attributes=True)


#Optional
class responseWallets(Wallets):
    id: int
    create_date: datetime

#Transaction
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

#Conversation
class Conversations(BaseModel):
    id: int
    user_id: int
    amount: float
    date: datetime

    model_config = ConfigDict(from_attributes=True)

#Chats
class Chats(BaseModel):
    id: int
    user_id: int
    message: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

#Transaction Category
class TransactionCategory(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class CreateTransactionCategory(BaseModel):
    name: str

#Transaction Type
class TransactionType(BaseModel):
    id: int
    name: str
    category_id: int

    model_config = ConfigDict(from_attributes=True)

#Chat
class Chat(BaseModel):
    chat : str = ""

#Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = ""