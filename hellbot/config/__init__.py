import os

from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()


API_HASH = os.environ.get("API_HASH", None)
API_ID = os.environ.get("API_ID", None)
ARQ_API_KEY = os.environ.get("ARQ_API_KEY", None)
ARQ_API_URL = "https://thearq.tech/"
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
BOT_USERNAME = os.environ.get("BOT_USERNAME", None)
BRANCH = "master"
DB_URI = os.environ.get("DATABASE_URL", None)
DURATION_LIMIT = os.environ.get("DURATION_LIMIT", "60")
HANDLER = os.environ.get("HANDLER", "/")
HELLBOT_SESSION = os.environ.get("HELLBOT_SESSION", None)
HEROKU_APIKEY = os.environ.get("HEROKU_APIKEY", None)
HEROKU_APPNAME = os.environ.get("HEROKU_APPNAME", None)
LOGGER_ID = int(os.environ.get("LOGGER_ID"))
OWNER = int(os.environ.get("OWNER"))
SUDO_USERS = list(map(int, os.environ.get("SUDO_USERS").split()))
THUMBNAIL = os.environ.get("THUMBNAIL", "https://")
UPSTREAM_REPO = os.environ.get("UPSTREAM_REPO", "https://github.com/HellBoy-OP/Music")
