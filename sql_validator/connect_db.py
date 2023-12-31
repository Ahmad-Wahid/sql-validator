
from __future__ import annotations

import click
from dotenv import load_dotenv
import psycopg2
import os


def get_env_variables():
    status = load_dotenv()
    if status is False:
        click.echo("Environment file is missing.")
        exit()
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    return database, user, password, host, port


def connect_db(
    database: str = None,
    user: str = None,
    password: str = None,
    host: str = "localhost",
    port: str = "5432",
) -> psycopg2:
    try:
        if not (database and user and password):
            database, user, password, host, port = get_env_variables()

        if database and user and password:
            conn = psycopg2.connect(
                database=database, user=user, password=password, host=host, port=port
            )
            return conn
        else:
            print("Database credentials not found in .env file")
    except Exception as e:
        print("An error occurred:", e)
