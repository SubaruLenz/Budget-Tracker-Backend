from datetime import timedelta, datetime, timezone
from typing import Annotated
from dotenv import load_dotenv

import os, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from app.database import baseModels, models
from app.database.database import get_db

#Get environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRATION = os.getenv("ACCESS_TOKEN_EXPIRATION")

#db: Session = Depends(get_db)

pwd_context = CryptContext(schemes = ["bcrypt_sha256"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#Verify password and hash password function
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#Hash password function
def get_password_hash(password):
    return pwd_context.hash(password)

#Get user from database
def get_user(username: str, db: Session):
    try:
        user = db.query(models.Users).filter_by(username=username).first()
        if user:
            user_dict = user.__dict__.copy()
            user_dict.pop('_sa_instance_state', None)
            # Map 'password' to 'hashed_password'
            user_dict['hashed_password'] = user_dict.pop('password')
            print(f"[User] {baseModels.UserInDB(**user_dict)}")
            return baseModels.UserInDB(**user_dict)
        else:
            print("[Error] User not found")
            return None
    except Exception as e:
        print(f"[Error] Error at get user. This error {e}")
        raise Exception

# Authenticate user function
def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Create access token function
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    if not SECRET_KEY or not ALGORITHM:
        raise RuntimeError("SECRET_KEY and ALGORITHM must be set in environment variables")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Get current user function
async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)], 
        database: Session = Depends(get_db)
    ):
    credentials_execption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if not SECRET_KEY or not ALGORITHM:
            raise RuntimeError("SECRET_KEY and ALGORITHM must be set in environment variables")
        else:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
        if username is None:
            raise credentials_execption
        if baseModels.TokenData is None:
            raise credentials_execption
        token_data = baseModels.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_execption
    user = get_user(username=token_data.username, db=database)
    if user is None:
        raise credentials_execption
    return user

#Optional for active user (Enabled/Disabled)
#async def get_current_active_user(
#  current_user: Annotated[baseModels.Users, Depends(get_current_user)]      
#):
#    if current_user.disabled:
#        raise HTTPException(status_code=400, detail="Inactive user")
#    return current_user
