#Libraries
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import null
from sqlalchemy.orm import Session
from typing import Annotated

#Dependecies
import app.authentication.jwt_manager as jwt_manager
from app.database.baseModels import Users as baseUsers, Wallets as baseWallets, responseWallets
from app.database.database import get_db
from app.database.models import Wallets, Users
from app.config.log_config import setup_config

#Routing
router = APIRouter(tags=["Wallets"])

#Logging
setup_config()
logger = logging.getLogger(__name__)

#User verification
def user_verification(
    current_user: baseUsers,
    db: Session
):
    user = db.query(Users).filter_by(username=current_user.username).first()

    if(not user):
        logger.error("User not found")
        raise HTTPException(status_code=404, detail="User not found")

#Routers
@router.get("/wallet/me")
def get_wallets(
    current_user: Annotated[baseUsers, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user_verification(current_user, db)

    wallets = db.query(Wallets).filter_by(user_id=current_user.id).all()
    if not wallets:
        return {"message": "No wallet found"}

    wallet_dicts = [
        responseWallets(**{k: v for k, v in wallet.__dict__.items() if k != '_sa_instance_state'})
        for wallet in wallets
    ]
    logger.info(f"[Wallets] - {wallet_dicts}")
    return {"wallets": wallet_dicts}

    
@router.post("/wallet/create")
def create_wallet(
    baseWallet: baseWallets,
    current_user: Annotated[baseUsers, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user_verification(current_user, db)

    new_wallet = Wallets(
        name=baseWallet.name,
        balance=baseWallet.balance,
        user_id=current_user.id
    )
    db.add(new_wallet)
    db.commit()
    db.refresh(new_wallet)
    logger.info("Create wallet successfully")
    return {"message": "Wallet created successfully"}

    
@router.get("/wallet/{wallet_id}")
def get_wallet_by_id(
    wallet_id: int,
    current_user: Annotated[baseUsers, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user_verification(current_user, db)

    wallet = db.query(Wallets).filter_by(id=wallet_id, user_id=current_user.id).first()
    if wallet:
        wallet_dict = {k: v for k, v in wallet.__dict__.items() if k != '_sa_instance_state'}
        return responseWallets(**wallet_dict)
    else:
        return {"message": "Wallet wrong id or not found"}

    
@router.put("/wallet/update/{wallet_id}")
def update_wallet(
    wallet_id: int,
    baseWallet: baseWallets,
    current_user: Annotated[baseUsers, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user_verification(current_user, db)

    wallet = db.query(Wallets).filter_by(id=wallet_id, user_id=current_user.id).first()
    if wallet:
        wallet.name = baseWallet.name
        wallet.balance = baseWallet.balance
        db.commit()
        logger.info("Update wallet successfully")
        return {"message": "Wallet updated successfully"}
    else:
        logger.error("Wallet not found")
        return {"error": "Wallet not found"}

    
@router.delete("/wallet/delete/{wallet_id}")
def delete_wallet(
    wallet_id: int,
    current_user: Annotated[baseUsers, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user_verification(current_user, db)

    wallet = db.query(Wallets).filter_by(id=wallet_id, user_id=current_user.id).first()
    if wallet:
        db.delete(wallet)
        db.commit()
        logger.info("[Success] Delete wallet successfully")
        return {"message": "Wallet deleted successfully"}
    else:
        logger.error("Wallet not found")
        return {"error": "Wallet not found"}

    