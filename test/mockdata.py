import datetime
from sqlalchemy.orm import Session
from app.database import models
from app.database.database import engine
from app.authentication.jwt_manager import get_password_hash

def create_mock_data():
    session = Session(bind=engine)

    print("Starting mock data insertion...")

    # ----------------------
    # 1. Add Users
    # ----------------------
    user1 = models.Users(
        username="johndoe",
        name="John Doe",
        email="john@example.com",
        password_hashed=get_password_hash("123"),
        create_date=datetime.datetime.now()
    )

    admin = models.Users(
        username="admin",
        name="Admin",
        email="admin@example.com",
        password_hashed=get_password_hash("admin"),
        create_date=datetime.datetime.now()
    )

    user2 = models.Users(
        username="janedoe",
        name="Jane Doe",
        email="jane@example.com",
        password_hashed=get_password_hash("abc123"),
        create_date=datetime.datetime.now()
    )

    user3 = models.Users(
        username="lazycat",
        name="Luna Cat",
        email="luna@example.com",
        password_hashed=get_password_hash("meowmeow"),
        create_date=datetime.datetime.now()
    )

    session.add_all([user1, admin, user2, user3])
    session.flush()

    print("Users inserted:", user1.username, admin.username, user2.username, user3.username)

    # ----------------------
    # 2. Add Wallets
    # ----------------------
    wallet1 = models.Wallets(
        name="John's Wallet",
        balance=1000.00,
        user_id=user1.id,
        create_date=datetime.datetime.now()
    )

    wallet2 = models.Wallets(
        name="Jane's Piggybank",
        balance=2500.00,
        user_id=user2.id,
        create_date=datetime.datetime.now()
    )

    wallet3 = models.Wallets(
        name="Luna's Secret Stash",
        balance=420.69,
        user_id=user3.id,
        create_date=datetime.datetime.now()
    )

    session.add_all([wallet1, wallet2, wallet3])
    session.flush()

    print("Wallets inserted:", wallet1.name, wallet2.name, wallet3.name)

    # ----------------------
    # 3. Add Categories
    # ----------------------
    category_food = models.TransactionCategories(name="Food")
    category_utilities = models.TransactionCategories(name="Utilities")
    category_entertainment = models.TransactionCategories(name="Entertainment")
    category_pets = models.TransactionCategories(name="Pets")

    session.add_all([category_food, category_utilities, category_entertainment, category_pets])
    session.flush()

    print("Transaction categories inserted:", category_food.name, category_utilities.name, category_entertainment.name, category_pets.name)

    # ----------------------
    # 4. Add Transaction Types
    # ----------------------
    type_groceries = models.TransactionType(name="Groceries", category_id=category_food.id)
    type_electric = models.TransactionType(name="Electric Bill", category_id=category_utilities.id)
    type_streaming = models.TransactionType(name="Netflix", category_id=category_entertainment.id)
    type_pet_food = models.TransactionType(name="Cat Food", category_id=category_pets.id)

    session.add_all([type_groceries, type_electric, type_streaming, type_pet_food])
    session.flush()

    print("Transaction types inserted:", type_groceries.name, type_electric.name, type_streaming.name, type_pet_food.name)

    # ----------------------
    # 5. Add Transactions
    # ----------------------
    transaction1 = models.Transactions(
        name="Grocery Shopping",
        amount=150.50,
        transaction_type_id=type_groceries.id,
        user_id=user1.id,
        wallet_id=wallet1.id,
        transaction_date=datetime.datetime.now()
    )

    transaction2 = models.Transactions(
        name="Netflix Monthly",
        amount=15.99,
        transaction_type_id=type_streaming.id,
        user_id=user2.id,
        wallet_id=wallet2.id,
        transaction_date=datetime.datetime.now()
    )

    transaction3 = models.Transactions(
        name="Cat Food - Fancy Feast",
        amount=40.00,
        transaction_type_id=type_pet_food.id,
        user_id=user3.id,
        wallet_id=wallet3.id,
        transaction_date=datetime.datetime.now()
    )

    session.add_all([transaction1, transaction2, transaction3])
    print("Transactions inserted:", transaction1.name, transaction2.name, transaction3.name)

    # ----------------------
    # 6. Add Conversations
    # ----------------------
    conversation1 = models.Conversations(
        user_id=user1.id,
        create_date=datetime.datetime.now(),
    )

    conversation2 = models.Conversations(
        user_id=user2.id,
        create_date=datetime.datetime.now(),
    )

    session.add_all([conversation1, conversation2])
    session.flush()

    print("Conversations created with IDs:", conversation1.id, conversation2.id)

    # ----------------------
    # 7. Add Chats
    # ----------------------
    chat1 = models.Chats(
        conversation_id=conversation1.id,
        role=models.ConversationRole.USER,
        content="Hey, how can I track my groceries?",
        create_date=datetime.datetime.now()
    )

    chat2 = models.Chats(
        conversation_id=conversation2.id,
        role=models.ConversationRole.USER,
        content="Can you remind me when my bills are due?",
        create_date=datetime.datetime.now()
    )

    session.add_all([chat1, chat2])
    session.flush()

    print("Chat messages inserted with IDs:", chat1.id, chat2.id)

    # ----------------------
    # Commit All Changes
    # ----------------------
    session.commit()
    print("Mock data insertion completed successfully.")
