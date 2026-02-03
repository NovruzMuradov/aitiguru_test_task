"""
Файл настроек приложения (конфигурация).
"""

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://username:password@localhost:5432/inventory_db"
)
