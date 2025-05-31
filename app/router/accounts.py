#Libraries
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

#Dependencies
import app.jwt_manager as jwt_manager
from app.jwt_manager import ACCESS_TOKEN_EXPIRATION
from ..database import baseModels, models
from ..database.database import get_db
from ..database.models import Users

router = APIRouter(tags=["Account Management"])

@router.post("/users/create")
def create_account(baseUser: baseModels.UserInDB, db: Session = Depends(get_db)):
    try:
        if (not db.query(Users).filter_by(username=f"{baseUser.username}").first() or not db.query(Users).filter_by(email=f"{baseUser.email}").first()):
            hash=jwt_manager.get_password_hash(baseUser.hashed_password)
            #clean_hash = hash.replace("$bcrypt-sha256$v=2,t=2b,r=12", "")
            new_account = models.Users(
                username=baseUser.username,
                name=baseUser.name,
                email=baseUser.email,
                password=hash,
                create_date=datetime.now(timezone.utc))
            db.add(new_account)
            db.commit()
            db.refresh(new_account)
            print("[Success] Create item successfully")
            print(f"[Hash] {hash}")
            return {"message": "Item created successfully"}
        else:
            print("[Error] Username exist or email")
            return {"error": "Username or email Exist"}
    except Exception as e:
        print(f"[Error] Error occurred while creating user {str(e)}")
        return {"error": str(e)}

#Obsolete update user function
@router.put("/user/update/{id}")
def update_user(id: int, baseUser: baseModels.UserInDB, db: Session = Depends(get_db)):
    user = db.query(Users).filter_by(id=f"{id}").first()
    hash = jwt_manager.get_password_hash(baseUser.hashed_password)
    try:
        if(user):
            user.username = baseUser.username
            user.name = baseUser.name
            user.email = baseUser.email
            user.password = hash
            db.merge(user)
            db.commit()
            print("[Success] Update item successfully")
            return {"message": "Item updated successfully"}
        else:
            print(f"[Error] This account doesn't exist")
            return {"error": "This account doesn't exist"}
    except Exception as e:
        print(f"[Error] Error while trying to update user")
        return {"error": str(e)}

#Obsolete clean hash function
@router.put("/user/clean/{id}")
def clean_hash(id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter_by(id=f"{id}").first()
    hash = "$bcrypt-sha256$v=2,t=2b,r=12"
    try:
        if(user):
            local_password = user.password
            if hash in user.password:
                user.password = local_password.replace(hash, "")
                db.merge(user)
                db.commit()
                print("[Success] This one is cleaned")
                return{"message": "This one is cleaned"}
            else:
                print("[Success] This one is already cleaned")
                return {"message":"This one is already cleaned"}
        print(f"[Error] This account doesn't exist")
        return {"error": "This account doesn't exist"}
    except Exception as e:
        print(f"[Error] Error while trying to update user")
        return {"error": str(e)}

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
        print("[Error] Please add Expiraion to environment file")
        raise Exception
    access_token = jwt_manager.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return baseModels.Token(access_token=access_token, token_type="bearer")

@router.get("/users/me/", response_model=baseModels.Users)
async def read_users_me(
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
):
    return current_user