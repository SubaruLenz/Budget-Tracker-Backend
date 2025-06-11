from fastapi import APIRouter
from . import accounts, transactions, wallets, category

routerManager = APIRouter()
routerManager.include_router(accounts.router)
routerManager.include_router(wallets.router)
routerManager.include_router(category.router)
routerManager.include_router(transactions.router)