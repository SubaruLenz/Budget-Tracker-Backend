import time
import psycopg2
from fastapi import FastAPI
from .database import models
from .database.database import engine, DATABASE_URL
from .router import router_manager

#Import mockdata script
from test.mockdata import create_mock_data

app = FastAPI()

#Operation
#models.Base.metadata.bind = engine

def create_database():
    print("Creating database tables...")
    models.Base.metadata.create_all(bind=engine)
    print("Creating database tables completed.")

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