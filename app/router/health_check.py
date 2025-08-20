from fastapi import APIRouter

router = APIRouter(tags=["Account Management"])

@router.get("/")
def health_check():
    return {"status": "healthy"}