from fastapi import APIRouter
from . import accounts, transactions, wallets

routerManager = APIRouter()
routerManager.include_router(accounts.router)
routerManager.include_router(wallets.router)
routerManager.include_router(transactions.router)