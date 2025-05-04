from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from database_mapping import User, Wallet, Transaction
from database_model import UserCreate, User, WalletCreate, Wallet, TransactionCreate, Transaction

app = FastAPI()

# Create a User
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get a User by ID
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Create a Wallet
@app.post("/wallets/", response_model=Wallet)
def create_wallet(wallet: WalletCreate, db: Session = Depends(get_db)):
    db_wallet = Wallet(**wallet.dict())
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet

# Get Wallets for a User
@app.get("/users/{user_id}/wallets", response_model=List[Wallet])
def get_user_wallets(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.wallets

# Create a Transaction
@app.post("/transactions/", response_model=Transaction)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    # Check if user and wallet exist
    db_user = db.query(User).filter(User.id == transaction.user_id).first()
    db_wallet = db.query(Wallet).filter(Wallet.id == transaction.wallet_id).first()
    if not db_user or not db_wallet:
        raise HTTPException(status_code=404, detail="User or Wallet not found")
    
    # Update wallet balance
    db_wallet.balance += transaction.amount
    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    db.refresh(db_wallet)  # Update wallet balance
    return db_transaction