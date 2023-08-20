from dotenv import load_dotenv
import psycopg2
import os

# Load environment variables from .env file
load_dotenv()

def connect_db():
    try:
        database = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")

        if database and user and password:
            conn = psycopg2.connect(
                database=database, user=user, password=password, host=host, port=port
            )
            return conn
        else:
            print("Database credentials not found in .env file")
    except Exception as e:
        print("An error occurred:", e)
