#Libraries
import logging
from fastapi import Depends
from sqlalchemy.orm import Session

#Dependencies
from app.database.database import get_db
from app.config.log_config import setup_config
from app.database.models import TransactionType
from app.llm.models.response_models import TransactionModel

#Logging
setup_config()
logger = logging.getLogger(__name__)


def get_transaction_types(db: Session):
    transaction_types = db.query(TransactionType).with_entities(TransactionType.id, TransactionType.name).all()

    if not transaction_types:
        logger.error("No transaction types found")
        raise Exception("No transaction types found")
    logger.info(f"Transaction types: {transaction_types}")
    verified_transaction_types: list[TransactionModel] = [
        TransactionModel(id=transaction_type.id, name=transaction_type.name) for transaction_type in transaction_types
    ]
    return verified_transaction_types

