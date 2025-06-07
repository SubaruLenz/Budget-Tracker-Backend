#Libraries
from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy import null
from sqlalchemy.orm import Session
from typing import Annotated

#Dependecies
import app.authentication.jwt_manager as jwt_manager
from app.database import baseModels
from app.database.database import get_db
from app.database.models import Transactions, Users

#Routing
router = APIRouter(tags=["Transactions"])

@router.get("/transaction/me")
async def get_transactions(
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter_by(username=current_user.username).first()
    if (user):
        transactions = db.query(Transactions).filter_by(id=user.id).first()
        print(transactions)
        if (transactions == None):
            return {"message": "No transaction"}
        else:
            return transactions
    else:
        print("[Error] User is found at get_transaction")
        return {"message": "User not found"}


#@router.post("/transaction/create")
#async def make_transactions(
#    baseTransaction: baseModels.Transactions,
#    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
#    db: Session = Depends(get_db),
#):
#    user = db.query(Users).filter_by(username=current_user.username).first()
#    if(user):
#
#    else:
#        print("[Error] User not found")
#        return {"message" : "User not found"}