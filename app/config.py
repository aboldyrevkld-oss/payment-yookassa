import os
from dotenv import load_dotenv

load_dotenv()

# YooKassa
YOOKASSA_SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
YOOKASSA_API_KEY = os.getenv("YOOKASSA_API_KEY")
YOOKASSA_API_URL = os.getenv("YOOKASSA_API_URL", "https://api.yookassa.ru/v3/payments")
YOOKASSA_SUCCESS_URL = os.getenv("YOOKASSA_SUCCESS_URL", "http://localhost:5173/success")
YOOKASSA_CANCEL_URL = os.getenv("YOOKASSA_CANCEL_URL", "http://localhost:5173/cancel")

# DB
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://payments:payments@postgres:5432/payments_db")

# Redis / Celery
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
