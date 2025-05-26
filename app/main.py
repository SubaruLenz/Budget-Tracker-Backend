import time
import psycopg2
from fastapi import FastAPI
from .database import models
from .database.database import engine, DATABASE_URL
from .router import router_manager

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

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