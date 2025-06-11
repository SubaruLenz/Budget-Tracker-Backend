#Libraries
from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy import null
from sqlalchemy.orm import Session
from typing import Annotated

#Dependecies
import app.authentication.jwt_manager as jwt_manager
from app.database import baseModels
from app.database.database import get_db
from app.database.models import TransactionCategories, Users

#Routing
router = APIRouter(tags=["Category"])

#User verification
def user_verification(
    current_user: baseModels.Users,
    db: Session
):
    user = db.query(Users).filter_by(username=current_user.username).first()

    if(not user):
        print("[Error] User not found")
        raise HTTPException(status_code=404, detail="User not found")

#Routers
@router.get("/categories", response_model=list[baseModels.TransactionCategory])
async def get_categories(
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):  
    user_verification(current_user, db)
    categories = db.query(TransactionCategories).all()
    baseCategories: list[baseModels.TransactionCategory] = []
    for category in categories:
        baseCategories.append(baseModels.TransactionCategory.model_validate(category))
    return baseCategories

@router.get("/category/{id}", response_model=baseModels.TransactionCategory)
def get_category_by_id(
    id: int,
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    #Verification
    user_verification(current_user, db)

    #Category search
    category = db.query(TransactionCategories).filter_by(id=id).first()
    if (not category):
        print("[error] Category not found")
        raise HTTPException(status_code=404, detail="Category not found")   
    return baseModels.TransactionCategory.model_validate(category)

@router.post("/category/create")
def create_category(
    base_category: baseModels.TransactionCategory,
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    #verification
    user_verification(current_user, db)

    #Only allow admin
    if (current_user.username != "admin"):
        print("[Error] Not admin try to delete category")
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
    base_category: baseModels.TransactionCategory,
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    #Verification
    user_verification(current_user, db)

    #Only allow admin
    if (current_user.username != "admin"):
        print("[Error] Not admin try to delete category")
        return {"error": "Unauthorized action"}

    #Update
    category = db.query(TransactionCategories).filter_by(id=id).first()
    if (not category):
        print("[Error] Category not found")
        return {"error": "Category not found"}

    category=base_category.name
    db.commit()
    return {"message": "Update category successfully"}

@router.delete("/category/delete/{id}")
def delete_category(
    id:int,
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    #Verification
    user_verification(current_user, db)

    #Only allow admin
    if (current_user.username != "admin"):
        print("[Error] Not admin try to delete category")
        return {"error": "Unauthorized action"}
    
    #Delete
    category = db.query(TransactionCategories).filter_by(id=id).first()
    if (not category):
        print("[Error] Category not found")
        return {"error": "Category not found"}
    db.delete(category)
    db.commit()
    print("[Success] Delete category successfully")
