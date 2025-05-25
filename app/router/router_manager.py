from fastapi import APIRouter
from . import test_table

routerManager = APIRouter()
routerManager.include_router(test_table.router)