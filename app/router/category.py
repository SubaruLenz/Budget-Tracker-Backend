#Libraries
import logging
from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy import null
from sqlalchemy.orm import Session
from typing import Annotated

#Dependecies
import app.authentication.jwt_manager as jwt_manager
from app.database.baseModels import Users as baseUsers, TransactionCategory as baseTransactionCategory, CreateTransactionCategory
from app.database.database import get_db
from app.database.models import TransactionCategories, Users
from app.config.log_config import setup_config

#Routing
router = APIRouter(tags=["Category"])

#Logging
setup_config()
logger = logging.getLogger(__name__)

#User verification
def user_verification(
    current_user: baseUsers,
    db: Session
):
    user = db.query(Users).filter_by(username=current_user.username).first()

    if(not user):
        logger.error("User not found")
        raise HTTPException(status_code=404, detail="User not found")

#Routers
@router.get("/categories", response_model=list[baseTransactionCategory])
async def get_categories(
    current_user: Annotated[baseUsers, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):  
    user_verification(current_user, db)
    categories = db.query(TransactionCategories).all()
    baseCategories: list[baseTransactionCategory] = []
    for category in categories:
        baseCategories.append(baseTransactionCategory.model_validate(category))
    return baseCategories

@router.get("/category/{id}", response_model=baseTransactionCategory)
def get_category_by_id(
    id: int,
    current_user: Annotated[baseUsers, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    #Verification
    user_verification(current_user, db)

    #Category search
    category = db.query(TransactionCategories).filter_by(id=id).first()
    if (not category):
        logger.error("Category not found")
        raise HTTPException(status_code=404, detail="Category not found")   
    return baseTransactionCategory.model_validate(category)

@router.post("/category/create")
def create_category(
    base_category: CreateTransactionCategory,
    current_user: Annotated[baseUsers, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    #verification
    user_verification(current_user, db)

    #Only allow admin
    if (current_user.username != "admin"):
        logger.error("Not admin try to delete category")
        return {"error": "Unauthorized action"}

    #Create category
    new_category = TransactionCategories(
        category=base_category.name
    )
    db.add(new_category)
    db.commit()
    db.refresh
    return {"message": "Create category successfully"}

@router.put("/category/update/{id}")
def update_category(
    id:int,
    base_category: CreateTransactionCategory,
    current_user: Annotated[baseUsers, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    #Verification
    user_verification(current_user, db)

    #Only allow admin
    if (current_user.username != "admin"):
        logger.error("Not admin try to delete category")
        return {"error": "Unauthorized action"}

    #Update
    category = db.query(TransactionCategories).filter_by(id=id).first()
    if (not category):
        logger.error("Category not found")
        return {"error": "Category not found"}

    category=base_category.name
    db.commit()
    return {"message": "Update category successfully"}

@router.delete("/category/delete/{id}")
def delete_category(
    id:int,
    current_user: Annotated[baseUsers, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    #Verification
    user_verification(current_user, db)

    #Only allow admin
    if (current_user.username != "admin"):
        logger.error("Not admin try to delete category")
        return {"error": "Unauthorized action"}
    
    #Delete
    category = db.query(TransactionCategories).filter_by(id=id).first()
    if (not category):
        logger.error("Category not found")
        return {"error": "Category not found"}
    db.delete(category)
    db.commit()
    logger.info("Delete category successfully")
