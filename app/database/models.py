import datetime, enum
from sqlalchemy import Integer, String, DateTime, Numeric, ForeignKey, Enum
from sqlalchemy.orm import Mapped, MappedColumn, relationship

from .database import Base, engine

class TransactionTypeEnum(enum.Enum):
    FOOD = "food"
    COMMUTE = "commute"
    OTHER = "other"

class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"autoload_with": engine}

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, nullable=False)
    username: Mapped[str] = MappedColumn(String(50), nullable=False)
    name: Mapped[str] = MappedColumn(String(100), nullable=False)
    email: Mapped[str] = MappedColumn(String(254), unique=True, nullable=False)
    password: Mapped[str] = MappedColumn(String(100), nullable=False)
    create_date: Mapped[DateTime] = MappedColumn(DateTime, default=datetime.datetime.now, nullable=False)

    user_wallet_fk = relationship("Wallets")
    user_transaction_fk = relationship("Transactions")
    user_conversation_fk = relationship("Conversations")

class Wallets(Base):
    __tablename__ = "wallets"
    __table_args__ = {"autoload_with": engine}

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = MappedColumn(String(100), nullable=False)
    user_id: Mapped[int] = MappedColumn(Integer, ForeignKey("users.id"))
    balance: Mapped[float] = MappedColumn(Numeric(10, 2))

    wallet_transaction_fk = relationship("Transactions")

class Transactions(Base):
    __tablename__ = "transactions"
    __table_args__ = {"autoload_with": engine}

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = MappedColumn(String(100), nullable=False)
    amount: Mapped[float] = MappedColumn(Numeric(10, 2))
    transaction_type: Mapped[TransactionTypeEnum] = MappedColumn(Enum(TransactionTypeEnum), default="other")
    user_id: Mapped[int] = MappedColumn(Integer, ForeignKey("users.id"))
    wallet_id: Mapped[int] = MappedColumn(Integer, ForeignKey("wallets.id"))
    transaction_date: Mapped[DateTime] = MappedColumn(DateTime, default=datetime.datetime, nullable=False)

class Conversations(Base):
    __tablename__ = "conversations"
    __table_args__ = {"autoload_with": engine}

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = MappedColumn(Integer, ForeignKey("users.id"))
    create_date: Mapped[DateTime] = MappedColumn(DateTime, nullable=True)

    conversations_chat_fk = relationship("Chats")

class Chats(Base):
    __tablename__ = "chats"
    __table_args__ = {"autoload_with": engine}

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, nullable=False)
    conversation_id: Mapped[int] = MappedColumn(Integer, ForeignKey("conversations.id"))
    texts: Mapped[str] = MappedColumn(String(255), nullable=False)
    create_date: Mapped[DateTime] = MappedColumn(DateTime, default=datetime.datetime.now, nullable=False)