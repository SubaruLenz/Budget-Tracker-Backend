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
from app.llm.functions.get_transaction_types_function import get_transaction_types

#Routing
router = APIRouter(tags=["Conversation"])

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
@router.get("/conversation/get")
async def get_conversation(
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user_verification(current_user, db)

    transaction_type = get_transaction_types(db)
    return {"transaction": transaction_type}


