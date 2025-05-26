import datetime
from fastapi import APIRouter, Depends
from passlib.hash import bcrypt_sha256
from sqlalchemy.orm import Session
from ..database import baseModels, models
from ..database.database import get_db

def encryptPassword(password):
    hash = bcrypt_sha256.hash(password)
    return hash

def verifyPassword(password, hash):
    return bcrypt_sha256.verify(password, hash)

router = APIRouter(tags=["Accounts"])

@router.post("/users", response_model=list[baseModels.Users])
def create_account(baseUser: baseModels.Users, db: Session = Depends(get_db)):
    try:
        hash=encryptPassword(baseUser.password)
        new_account = models.Users(
            username=baseUser.username,
            email=baseUser.email,
            password=hash,
            create_date=datetime.datetime.now())
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        print("[Success] Create item successfully")
        print("[Hash] {hash}")
        return {"message": "Item created successfully", "data": new_account}
    except Exception as e:
        print(f"[Error] Error occurred while creating item {str(e)}")
        return {"error": str(e)}