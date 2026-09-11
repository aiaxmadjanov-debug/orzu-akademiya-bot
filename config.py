import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Majburiy obuna kanallari
REQUIRED_CHANNELS = [
    {
        "chat_id": "@orzuakademiya",
        "name": "🌟 ORZU AKADEMIYA",
        "url": "https://t.me/orzuakademiya"
    }
]

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN .env faylida topilmadi!")

if not ADMIN_ID:
    raise ValueError("ADMIN_ID .env faylida topilmadi!")