import datetime
from sqlalchemy import Integer, String, DateTime, Numeric, ForeignKey, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from .database import Base, engine

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
    __table_args__ = {"autoload_with": engine}

class Transactions(Base):
    __tablename__ = "transactions"
    __table_args__ = {"autoload_with": engine}

class Wallets(Base):
    __tablename__ = "wallets"
    __table_args__ = {"autoload_with": engine}

class Conversations(Base):
    __tablename__ = "conversations"
    __table_args__ = {"autoload_with": engine}

class Chats(Base):
    __tablename__ = "chats"
    __table_args__ = {"autoload_with": engine}

class TransactionCategories(Base):
    __tablename__ = "transaction_categories"
    __table_args__ = {"autoload_with": engine}

class TransactionType(Base):
    __tablename__ = "transaction_types"
    __table_args__ = {"autoload_with": engine}