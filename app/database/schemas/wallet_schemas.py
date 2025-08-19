from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime

class Wallets(BaseModel):
    name: str
    balance: Decimal = Decimal(0.00)
    model_config = ConfigDict(from_attributes=True)

class responseWallets(Wallets):
    id: int
    create_date: datetime