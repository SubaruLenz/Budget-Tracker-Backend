import time
import psycopg2
from fastapi import FastAPI
from app.database import models
from app.database.database import engine, DATABASE_URL
from app.router import router_manager

#Import mockdata script
from test.mockdata import create_mock_data

app = FastAPI()

#Operation
#models.Base.metadata.bind = engine

def clear_database():
    #Development
    print("Dropping database tables...")
    models.Base.metadata.drop_all(bind=engine)
    print("Dropping database tables completed.")

def create_database():
    print("Creating database tables...")
    models.Base.metadata.create_all(bind=engine)
    print("Creating database tables completed.")

def run_mock():
    print("Inserting mock data...")
    create_mock_data()
    print("Mock data insertion completed.")

#Input to choose (test)
key_input = ""
while (key_input != "y" and key_input != "n"):
    key_input = input("Clear database and input mock data?(y/n): ")
else:
    if (key_input == "y"):
        clear_database()
        create_database()
        run_mock()
    else:
        create_database()

app = FastAPI()

def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            print(f"Database is connected")
            break
        except Exception as e:
            print(f"Error connecting to database: {e}")
            time.sleep(15)

app.include_router(router_manager.routerManager)