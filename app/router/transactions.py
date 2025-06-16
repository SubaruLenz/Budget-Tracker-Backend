#Libraries
import logging
from fastapi import APIRouter, Depends
from sqlalchemy import null
from sqlalchemy.orm import Session
from typing import Annotated

#Dependecies
import app.authentication.jwt_manager as jwt_manager
from app.database import baseModels
from app.database.database import get_db
from app.database.models import Transactions, Users
from app.config.log_config import setup_config

#Routing
router = APIRouter(tags=["Transactions"])

#Logging
setup_config()
logger = logging.getLogger(__name__)

#Routers
@router.get("/transaction/me")
async def get_transactions(
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter_by(username=current_user.username).first()
    if (user):
        transactions = db.query(Transactions).filter_by(id=user.id).first()
        logger.info(f"[Transactions] - {transactions}")
        if (transactions == None):
            logger.info("No transactions")
            return {"message": "No transaction"}
        else:
            return transactions
    else:
        logger.error("User not found")
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