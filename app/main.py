import time
import psycopg2
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import models
from .database.database import engine, DATABASE_URL
from .config.log_config import setup_config
from .router import router_manager

app = FastAPI()

#Operation
#models.Base.metadata.bind = engine

#Log config module
setup_config()

#Create database
logging.info("Creating database tables...")
models.Base.metadata.create_all(bind=engine)
logging.info("Creating database tables completed.")

def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            logging.info(f"Database is connected")
            break
        except Exception as e:
            logging.info(f"Error connecting to database: {e}")
            time.sleep(15)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_manager.routerManager)