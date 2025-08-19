#Libraries
import logging
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

#Dependencies
import app.authentication.jwt_manager as jwt_manager
from app.authentication.jwt_manager import ACCESS_TOKEN_EXPIRATION
from app.database import baseModels
from app.database.database import get_db
from app.database.models import Users
from app.config.log_config import setup_config

router = APIRouter(tags=["Account Management"])

#Logging
setup_config()
logger = logging.getLogger(__name__)

@router.post("/token")
async def login_for_accept_token(
        from_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
) -> baseModels.Token:
    user = jwt_manager.authenticate_user(from_data.username, from_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if (ACCESS_TOKEN_EXPIRATION is not None):
        expiration = float(ACCESS_TOKEN_EXPIRATION)
        access_token_expires=timedelta(minutes=expiration)
    else:
        logger.critical("[Error] Please add Expiraion to environment file")
        raise Exception
    access_token = jwt_manager.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return baseModels.Token(access_token=access_token, token_type="bearer")

@router.post("/users/create")
def create_account(baseUser: baseModels.CreateUser, db: Session = Depends(get_db)):
    try:
        if (not db.query(Users).filter_by(username=f"{baseUser.username}").first() or not db.query(Users).filter_by(email=f"{baseUser.email}").first()):
            hash=jwt_manager.get_password_hash(baseUser.hashed_password)
            new_account = Users(
                username=baseUser.username,
                name=baseUser.name,
                email=baseUser.email,
                password_hashed=hash,
                create_date=datetime.now(timezone.utc))
            db.add(new_account)
            db.commit()
            db.refresh(new_account)
            logger.info("Create account successfully")
            logger.info(f"[Hash] - {hash}")
            return {"message": "Item created successfully"}
        else:
            logger.error("Username exist or email")
            return {"error": "Username or email Exist"}
    except Exception as e:
        logger.exception(f"Error occurred while creating user {str(e)}")
        return {"error": str(e)}

@router.get("/users/me/", response_model=baseModels.Users)
async def read_users_me(
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
):
    return current_user

@router.put("/users/update/password", tags=["Obsolete"])
async def account_update_password(
    baseUser: baseModels.UserInDB,
    db: Session = Depends(get_db),
):
    user = db.query(Users).filter_by(username=baseUser.username).first()
    hash = jwt_manager.get_password_hash(baseUser.hashed_password)
    try:
        if(user):
            if (user.username == baseUser.username):
                if (user.email == baseUser.email):
                    user.name = baseUser.name
                    user.password_hashed = hash
                    db.merge(user)
                    db.commit()
                    logger.info("Update account successfully")
                    return {"message": "Account updated successfully"}
                else:
                    logger.error("Email doesn't match")
                    return {"error": "Email doesn't match"}
            else:
                logger.error("Username doesn't match")
                return {"error": "Username doesn't match"}
        else:
            logger.error(f"This account doesn't exist")
            return {"error": "This account doesn't exist"}
    except Exception as e:
        logger.exception(f"Error while trying to update user")
        return {"error": str(e)}

@router.put("/users/update")
async def account_update(
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    baseUser: baseModels.UpdateUser,
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter_by(username=current_user.username).first()
    hash = jwt_manager.get_password_hash(baseUser.hashed_password)
    try:
        if(not user):
            logger.error(f"This account doesn't exist")
            return {"error": "This account doesn't exist"}
        if (user.username != current_user.username):
            logger.error("Username doesn't match")
            return {"error": "Username doesn't match"}
        
        user.name = baseUser.name
        user.email = baseUser.email
        user.password_hashed = hash
        db.merge(user)
        db.commit()
        logger.info("Update item successfully")
        return {"message": "Account updated successfully"}
    except Exception as e:
        logger.exception(f"Error while trying to update user")
        return {"error": str(e)}

@router.delete("/users/delete")
async def account_delete(
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter_by(username=current_user.username).first()
    try:
        if(user):
            db.delete(user)
            db.commit()
            logger.info("Delete Account successfully")
            return {"message": "Account deleted successfully"}
        else:
            logger.error(f"This account doesn't exist")
            return {"error": "This account doesn't exist"}
    except Exception as e:
        logger.exception(f"Error while trying to delete user")
        return {"error": str(e)}