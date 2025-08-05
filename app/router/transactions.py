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
    user_verification(current_user, db) #User

    type_id = db.query(TransactionType).filter_by(id=baseTransaction.transaction_type_id).first()
    verify_wallet_id = db.query(Wallets).filter_by(id=baseTransaction.wallet_id).first()

    if (not type_id or not verify_wallet_id):
        logger.error("Invalid ID")

    new_transaction = Transactions(
        name = baseTransaction.name,
        amount = baseTransaction.amount,
        transaction_type_id = baseTransaction.transaction_type_id,
        wallet_id = baseTransaction.wallet_id,
        user_id=current_user.id
    )
    db.add(new_transaction)
    db.commit()
    db.refresh
    return {"message": f"New transaction created successfully with id: {new_transaction.id}"}

@router.put("/transaction/update/{id}")
def update_transaction (
    id: int,
    baseTransaction: baseModels.Transactions,
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    
    #Verification
    user_verification(current_user, db)

    transaction = db.query(Transactions).filter_by(id=id).first()

    if (not transaction):
        logger.error("Transaction not found")
        return {"error": "Transaction not found"}
    if (transaction.user_id != current_user.id):
        logger.error("Unauthorized action")
        return {"error": "Unauthorized action"}

    transaction.name = baseTransaction.name
    transaction.amount = baseTransaction.amount
    transaction.transaction_type_id = baseTransaction.transaction_type_id
    db.commit()
    db.refresh(transaction)
    return {"meessage": f"Update successfully transaction {id}"}

@router.delete("/transaction/delete/{id}")
def delete_transaction(
    id: int,
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    
    #Verification
    user_verification(current_user, db)

    transaction = db.query(Transactions).filter_by(id=id).first()

    if (not transaction):
        logger.error("Transaction not found")
        return {"error": "Transaction not found"}
    if (transaction.user_id != current_user.id):
        logger.error("Unauthorized action")
        return {"error": "Unauthorized action"}
    
    db.delete(transaction)
    db.commit()
    db.refresh
    logger.info(f"Transaction deleted ID: {id}")
    return{"message": f"Transaction deleted sucessfully with ID: {id}"}