from fastapi import APIRouter
from . import accounts, transactions, wallets, category, conversation, health_check

routerManager = APIRouter()
routerManager.include_router(health_check.router)
routerManager.include_router(accounts.router)
routerManager.include_router(wallets.router)
routerManager.include_router(transactions.router)
routerManager.include_router(category.router)
routerManager.include_router(conversation.router)
