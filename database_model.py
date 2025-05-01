from pydantic import BaseModel, constr
from typing import Annotated, List, Optional
from datetime import datetime
from decimal import Decimal

# Users
class UserBase(BaseModel):
    name: Annotated[str, constr(max_length=100, strip_whitespace=True)]
    username: Annotated[str, constr(max_length=100, strip_whitespace=True)]
    password: Annotated[str, constr(max_length=100, strip_whitespace=True)]

class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    id: int
    create_date: datetime

    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy

class User(UserInDB):
    wallets: Optional[List["Wallet"]] = []  # Relationship: user_wallet
    transactions: Optional[List["Transaction"]] = []  # Relationship: user_transaction

# Wallets
class WalletBase(BaseModel):
    name: Annotated[str, constr(max_length=100, strip_whitespace=True)]
    balance: Decimal = Decimal("0.00")
    user_id: int  # Foreign key to users.id

class WalletCreate(WalletBase):
    pass

class WalletInDB(WalletBase):
    id: int
    create_date: datetime

    class Config:
        from_attributes = True

class Wallet(WalletInDB):
    transactions: Optional[List["Transaction"]] = []  # Relationship: transaction_wallet

# Transactions
class TransactionBase(BaseModel):
    name: Annotated[str, constr(max_length=100, strip_whitespace=True)]
    amount: Decimal
    user_id: int  # Foreign key to users.id
    wallet_id: int  # Foreign key to wallets.id

class TransactionCreate(TransactionBase):
    pass

class TransactionInDB(TransactionBase):
    id: int
    create_date: datetime

    class Config:
        from_attributes = True

class Transaction(TransactionInDB):
    pass