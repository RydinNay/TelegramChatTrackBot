import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
MODE = os.getenv("MODE", "polling")  # или webhook
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")

CHANNEL = os.getenv("CHANNEL", "")
INVITE_LINK = os.getenv("INVITE_LINK", "")
ADMIN_START_PARAM = os.getenv("ADMIN_START_PARAM", "")

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "mydatabase")

DB_URL = os.getenv("ASYNC_DB_URL")
