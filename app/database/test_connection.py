from psycopg2 import connect, OperationalError
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load .env file
load_dotenv()

# Get DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

def test_connection():
    if not DATABASE_URL:
        logging.error("DATABASE_URL is not set. Please check your .env file.")
        return
    try:
        # Establish connection
        connect(DATABASE_URL)
        logging.info("Connection successful!")
    except OperationalError as e:
        logging.error(f"Database connection failed: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_connection()