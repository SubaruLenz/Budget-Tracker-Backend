#Libraries
from fastapi import APIRouter, Depends
from sqlalchemy import null
from sqlalchemy.orm import Session
from typing import Annotated

#Dependecies
import app.authentication.jwt_manager as jwt_manager
from app.database import baseModels
from app.database.database import get_db
from app.database.models import Wallets, Users

#Routing
router = APIRouter(tags=["Wallets"])

@router.get("/wallet/me")
def get_wallets(
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter_by(username=current_user.username).first()
    if (user):
        wallets: list[Wallets] = db.query(Wallets).filter_by(user_id=user.id).all()
        wallet_dicts = []
        if (wallets == None):
            return{"message": "No wallet found"}
        else:
            for wallet in wallets:
                wallet_dict = wallet.__dict__.copy()
                wallet_dict.pop('_sa_instance_state', None)
                wallet_dicts.append(baseModels.responseWallets(**wallet_dict))
            print(f"[Wallets] {wallet_dicts}")
            return {"wallets": wallet_dicts}
    else:
        print("[Error] User not found")
        return{"error":"user not found"}
    
@router.post("/wallet/create")
def create_wallet(
    baseWallet: baseModels.Wallets,
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter_by(username=current_user.username).first()
    if (user):
        new_wallet = Wallets(
            name=baseWallet.name,
            balance=baseWallet.balance,
            user_id=current_user.id
        )
        db.add(new_wallet)
        db.commit()
        db.refresh(new_wallet)
        print("[Success] Create wallet successfully")
        return {"message": "Wallet created successfully"}
    else:
        print("[Error] User not found")
        return {"error": "User not found"}
    
@router.get("/wallet/{wallet_id}")
def get_wallet_by_id(
    wallet_id: int,
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter_by(username=current_user.username).first()
    if (user):
        wallet = db.query(Wallets).filter_by(id=wallet_id, user_id=user.id).first()
        if (wallet):
            wallet_dict = wallet.__dict__.copy()
            wallet_dict.pop('_sa_instance_state', None)
            return baseModels.responseWallets(**wallet_dict)
        else:
            return {"message": "Wallet wrong id or not found"}
    else:
        return{"error":"user not found"}
    
@router.put("/wallet/update/{wallet_id}")
def update_wallet(
    wallet_id: int,
    baseWallet: baseModels.Wallets,
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter_by(username=current_user.username).first()
    if (user):
        wallet = db.query(Wallets).filter_by(id=wallet_id, user_id=user.id).first()
        if (wallet):
            wallet.name = baseWallet.name
            wallet.balance = baseWallet.balance
            db.commit()
            print("[Success] Update wallet successfully")
            return {"message": "Wallet updated successfully"}
        else:
            print("[Error] Wallet not found")
            return {"error": "Wallet not found"}
    else:
        print("[Error] User not found")
        return {"error": "User not found"}
    
@router.delete("/wallet/delete/{wallet_id}")
def delete_wallet(
    wallet_id: int,
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter_by(username=current_user.username).first()
    if (user):
        wallet = db.query(Wallets).filter_by(id=wallet_id, user_id=user.id).first()
        if (wallet):
            db.delete(wallet)
            db.commit()
            print("[Success] Delete wallet successfully")
            return {"message": "Wallet deleted successfully"}
        else:
            print("[Error] Wallet not found")
            return {"error": "Wallet not found"}
    else:
        print("[Error] User not found")
        return {"error": "User not found"}
    