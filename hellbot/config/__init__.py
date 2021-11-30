import os

from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()


API_HASH = os.environ.get("API_HASH", None)
API_ID = os.environ.get("API_ID", None)
ARQ_API_KEY = os.environ.get("ARQ_API_KEY", None)
ARQ_API_URL = "https://grambuilders.tech"
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
BOT_USERNAME = os.environ.get("BOT_USERNAME", None)
DB_URI = os.environ.get("DATABASE_URL", None)
DURATION_LIMIT = os.environ.get("DURATION_LIMIT", "60")
HANDLER = os.environ.get("HANDLER", "/")
HELLBOT_SESSION = os.environ.get("HELLBOT_SESSION", None)
LOGGER_ID = int(os.environ.get("LOGGER_ID"))
OWNER = int(os.environ.get("OWNER"))
SUDO_USERS = list(map(int, os.environ.get("SUDO_USERS").split()))
THUMB_URL = os.environ.get("THUMBNAIL", "https://telegra.ph/file/3534633043e5f28f3f26b.jpg")
