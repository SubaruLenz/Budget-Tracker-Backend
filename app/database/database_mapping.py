from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# Users
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    create_date = Column(DateTime, default=datetime.now)

    wallets = relationship("Wallet", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

# Wallets
class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    balance = Column(Numeric(10, 2), default=0.00)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    create_date = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="wallets")
    transactions = relationship("Transaction", back_populates="wallet")

# Transactions
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    create_date = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="transactions")
    wallet = relationship("Wallet", back_populates="transactions")