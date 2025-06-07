import datetime
from sqlalchemy.orm import Session
from app.database import models 
from app.database.database import engine
 # adjust the import path to your models module

def create_mock_data ():
    # Start a DB session
    session = Session(bind=engine)
    
    print("Inserting mock data...")
    
    # ----------------------
    # 1. Add Users
    # ----------------------
    user1 = models.Users(
        username="johndoe",
        name="John Doe",
        email="john@example.com",
        password="hashed_password",  # Assume already hashed in real use
        create_date=datetime.datetime.now()
    )
    session.add(user1)
    session.flush()  # Get user1.id
    
    print("✅ User added:", user1.username)
    
    # ----------------------
    # 2. Add Wallet
    # ----------------------
    wallet1 = models.Wallets(
        name="John's Wallet",
        balance=1000.00,
        user_id=user1.id,
        create_date=datetime.datetime.now()
    )
    session.add(wallet1)
    session.flush()
    
    print("✅ Wallet added:", wallet1.name)
    
    # ----------------------
    # 3. Add Transaction Categories
    # ----------------------
    category_food = models.TransactionCategories(category="Food")
    category_utilities = models.TransactionCategories(category="Utilities")
    session.add_all([category_food, category_utilities])
    session.flush()
    
    print("✅ Categories added:", category_food.category, category_utilities.category)
    
    # ----------------------
    # 4. Add Transaction Types
    # ----------------------
    type_groceries = models.TransactionType(name="Groceries", category_id=category_food.id)
    type_electric = models.TransactionType(name="Electric Bill", category_id=category_utilities.id)
    session.add_all([type_groceries, type_electric])
    session.flush()
    
    print("✅ Transaction types added:", type_groceries.name, type_electric.name)
    
    # ----------------------
    # 5. Add Transactions
    # ----------------------
    transaction1 = models.Transactions(
        name="Grocery Shopping",
        amount=150.50,
        income=False,
        transaction_type_id=type_groceries.id,
        user_id=user1.id,
        wallet_id=wallet1.id,
        transaction_date=datetime.datetime.now()
    )
    session.add(transaction1)
    
    print("✅ Transaction added:", transaction1.name)
    
    # ----------------------
    # 6. Add Conversation
    # ----------------------
    conversation1 = models.Conversations(
        user_id=user1.id,
        create_date=datetime.datetime.now(),
        role="USER"  # Assuming Enum is set up as string values
    )
    session.add(conversation1)
    session.flush()
    
    print("✅ Conversation added with ID:", conversation1.id)
    
    # ----------------------
    # 7. Add Chat
    # ----------------------
    chat1 = models.Chats(
        conversation_id=conversation1.id,
        texts="Hey, how can I track my groceries?",
        create_date=datetime.datetime.now()
    )
    session.add(chat1)
    
    print("✅ Chat added with ID:", chat1.id)
    
    # ----------------------
    # Commit All Changes
    # ----------------------
    session.commit()
    print("✅ Mock data inserted.")
