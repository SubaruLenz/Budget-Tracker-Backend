#Libraries
import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated

#Dependecies
import app.authentication.jwt_manager as jwt_manager
from app.database import baseModels
from app.database.database import get_db
from app.database.models import Transactions, Users, TransactionType, Wallets
from app.config.log_config import setup_config

#Routing
router = APIRouter(tags=["Transactions"])

#Logging
setup_config()
logger = logging.getLogger(__name__)

#User verification
def user_verification(
    current_user: baseModels.Users,
    db: Session
):
    user = db.query(Users).filter_by(username=current_user.username).first()

    if(not user):
        logger.error("User not found")
        raise HTTPException(status_code=404, detail="User not found")

#Routers
@router.get("/transaction/me", response_model=dict[str, list[baseModels.ResponseTransactions]])
async def get_transactions(
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):  
    user_verification(current_user, db)

    transactions = db.query(Transactions).filter_by(user_id=current_user.id).all()
    
    verified_transations: list[baseModels.ResponseTransactions] = [
        baseModels.ResponseTransactions.model_validate(transaction) for transaction in transactions]
    
    return {"transactions": verified_transations}



@router.post("/transaction/create")
def create_transaction(
    baseTransaction: baseModels.CreateTransaction,
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    #Verification
    user_verification(current_user, db)

    type_id = db.query(TransactionType).filter_by(id=baseTransaction.transaction_type_id).first()
    wallet = db.query(Wallets).filter_by(id=baseTransaction.wallet_id, user_id=current_user.id).first()

    if not type_id or not wallet:
        logger.error("Invalid transaction type or wallet ID")
        raise HTTPException(status_code=404, detail="Invalid transaction type or wallet ID")

    # Create transaction
    new_transaction = Transactions(
        name=baseTransaction.name,
        amount=baseTransaction.amount,
        transaction_type_id=baseTransaction.transaction_type_id,
        wallet_id=baseTransaction.wallet_id,
        user_id=current_user.id
    )
    
    # Update wallet balance
    wallet.balance += baseTransaction.amount
    
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    return {"message": f"Transaction created and wallet balance updated. New balance: {wallet.balance}"}

@router.put("/transaction/update/{id}")
def update_transaction(
    id: int,
    baseTransaction: baseModels.Transactions,
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user_verification(current_user, db)

    transaction = db.query(Transactions).filter_by(id=id, user_id=current_user.id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    wallet = db.query(Wallets).filter_by(id=transaction.wallet_id).first()
    
    # Revert old amount and apply new amount
    wallet.balance = wallet.balance - transaction.amount + baseTransaction.amount
    
    transaction.name = baseTransaction.name
    transaction.amount = baseTransaction.amount
    transaction.transaction_type_id = baseTransaction.transaction_type_id
    
    db.commit()
    return {"message": f"Transaction updated. New wallet balance: {wallet.balance}"}

@router.delete("/transaction/delete/{id}")
def delete_transaction(
    id: int,
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user_verification(current_user, db)

    transaction = db.query(Transactions).filter_by(id=id, user_id=current_user.id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    wallet = db.query(Wallets).filter_by(id=transaction.wallet_id).first()
    
    # Revert transaction amount from wallet
    wallet.balance -= transaction.amount
    
    db.delete(transaction)
    db.commit()
    
    return {"message": f"Transaction deleted. New wallet balance: {wallet.balance}"}