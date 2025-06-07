import datetime
from sqlalchemy import Integer, String, DateTime, Numeric, ForeignKey, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from .database import Base

#Lazy option
#__table_args__ = {"autoload_with": engine}

class ConversationRole(enum.Enum):
    USER = "USER"
    SYSTEM = "SYSTEM"

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    create_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now, nullable=False
    )

    wallets = relationship("Wallets", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transactions", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversations", back_populates="user", cascade="all, delete-orphan")

class Wallets(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    balance: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0, nullable=False)
    create_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now, nullable=False
    )

    user = relationship("Users", back_populates="wallets")
    transactions = relationship("Transactions", back_populates="wallet", cascade="all, delete-orphan")

class Transactions(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    income: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    transaction_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("transaction_type.id", ondelete="SET DEFAULT"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    wallet_id: Mapped[int] = mapped_column(Integer, ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False)
    transaction_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now, nullable=False
    )

    user = relationship("Users", back_populates="transactions")
    wallet = relationship("Wallets", back_populates="transactions")
    transaction_type = relationship("TransactionType", back_populates="transactions")

class Conversations(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[ConversationRole] = mapped_column(Enum(ConversationRole), nullable=False)
    create_date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, nullable=False)

    user = relationship("Users", back_populates="conversations")
    chats = relationship("Chats", back_populates="conversation", cascade="all, delete-orphan")

class Chats(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    conversation_id: Mapped[int] = mapped_column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    texts: Mapped[str] = mapped_column(String(100), nullable=False)
    create_date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, nullable=False)

    conversation = relationship("Conversations", back_populates="chats")

class TransactionCategories(Base):
    __tablename__ = "transaction_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)

    transaction_types = relationship("TransactionType", back_populates="category", cascade="all, delete-orphan")

class TransactionType(Base):
    __tablename__ = "transaction_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("transaction_categories.id", ondelete="CASCADE"), nullable=True)

    category = relationship("TransactionCategories", back_populates="transaction_types")
    transactions = relationship("Transactions", back_populates="transaction_type", cascade="all, delete-orphan")