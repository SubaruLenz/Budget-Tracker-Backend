from decimal import Decimal
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Numeric, ForeignKey, Boolean, Enum
from sqlalchemy.orm import Mapped,DeclarativeBase, mapped_column, relationship
import enum

from .database import engine

# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

#Lazy option
#__table_args__ = {"autoload_with": engine}

#class Users(Base):
#    __tablename__ = "users"
#
#    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
#    username: Mapped[str] = mapped_column(String(100), nullable=False)
#    name: Mapped[str] = mapped_column(String(100), nullable=False)
#    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
#    password: Mapped[str] = mapped_column(String(100), nullable=False)
#    create_date: Mapped[datetime.datetime] = mapped_column(
#        DateTime, default=datetime.datetime.now, nullable=False
#    )
#
#    wallets = relationship("Wallets", back_populates="user", cascade="all, delete-orphan")
#    transactions = relationship("Transactions", back_populates="user", cascade="all, delete-orphan")
#    conversations = relationship("Conversations", back_populates="user", cascade="all, delete-orphan")

class Users(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hashed: Mapped[str] = mapped_column(String(1000), nullable=False)
    create_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    transactions: Mapped[list["Transactions"]] = relationship(back_populates="user")
    wallets: Mapped[list["Wallets"]] = relationship(back_populates="user")
    conversations: Mapped[list["Conversations"]] = relationship(back_populates="user")

class Transactions(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    transaction_type_id: Mapped[int] = mapped_column(ForeignKey("transaction_types.id", ondelete="RESTRICT"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE")) #user_transaction_fk
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id", ondelete="CASCADE")) #wallet_transaction_fk
    transaction_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    user: Mapped["Users"] = relationship(back_populates="transactions")
    wallet: Mapped["Wallets"] = relationship(back_populates="transactions")
    transaction_type: Mapped["TransactionType"] = relationship(back_populates="transactions")

class Wallets(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False, server_default="My wallet")
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE")) #user_wallet_fk
    create_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    user: Mapped["Users"] = relationship(back_populates="wallets")
    transactions: Mapped[list["Transactions"]] = relationship(back_populates="wallet")

class ConversationRole(enum.Enum):
    USER = "USER"
    SYSTEM = "SYSTEM"

class Conversations(Base):
    __tablename__ = "conversations"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE")) #user_conversation_fk
    create_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    user: Mapped["Users"] = relationship(back_populates="conversations")
    chats: Mapped[list["Chats"]] = relationship(back_populates="conversation")

class Chats(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id", ondelete="CASCADE")) #conversation_chat_fk
    role: Mapped[ConversationRole] = mapped_column(
        Enum(ConversationRole), name="role",nullable=False)
    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    conversation: Mapped["Conversations"] = relationship(back_populates="chats")

class TransactionType(Base):
    __tablename__ = "transaction_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("transaction_categories.id", ondelete="RESTRICT"))

    transactions: Mapped["Transactions"] = relationship(back_populates="transaction_type")

class TransactionCategories(Base):
    __tablename__ = "transaction_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)