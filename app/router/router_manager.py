from fastapi import APIRouter
from . import accounts

routerManager = APIRouter()
routerManager.include_router(accounts.router)