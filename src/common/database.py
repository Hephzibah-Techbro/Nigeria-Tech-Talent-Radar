import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


# Locate the project's root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Load database settings from the project's .env file
load_dotenv(BASE_DIR / ".env")


def get_db_connection():
    """Connect to the project's PostgreSQL database."""

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    return connection
