from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import baseModels, models
from ..database.database import get_db

router = APIRouter(tags=["CRUD Operations"])

