import datetime
from fastapi import APIRouter, Depends
from passlib.hash import bcrypt_sha256
from sqlalchemy.orm import Session
from ..database import baseModels, models
from ..database.database import get_db
from ..database.models import Users

def encryptPassword(password):
    hash = bcrypt_sha256.hash(password)
    return hash

def verifyPassword(password, hash):
    return bcrypt_sha256.verify(password, hash)

router = APIRouter(tags=["Account Management"])

@router.post("/users/create")
def create_account(baseUser: baseModels.Users, db: Session = Depends(get_db)):
    try:
        if (not db.query(Users).filter_by(username=f"{baseUser.username}").first() or not db.query(Users).filter_by(email=f"{baseUser.email}").first()):
            hash=encryptPassword(baseUser.password)
            clean_hash = hash.replace("$bcrypt-sha256$v=2,t=2b,r=12", "")
            new_account = models.Users(
                username=baseUser.username,
                name=baseUser.name,
                email=baseUser.email,
                password=clean_hash,
                create_date=datetime.datetime.now())
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
    
#@router.put("/user/update/{id}")
#def update_user(id: int, baseUser: baseModels.Users, db: Session = Depends(get_db)):
#    user = db.query(Users).filter_by(id=f"{id}").first()
#    try:
#        if(user):
#            
#        else:
#            print(f"[Error] This account doesn't exist")
#            return {"error": "This account doesn't exist"}
#    except Exception as e:
#        print(f"[Error] Error while trying to update user")
#        return {"error": str(e)}

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
        else:
            print(f"[Error] This account doesn't exist")
            return {"error": "This account doesn't exist"}
    except Exception as e:
        print(f"[Error] Error while trying to update user")
        return {"error": str(e)}

#@router.get("/users")
#def get_user():