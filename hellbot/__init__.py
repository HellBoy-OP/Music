from pyrogram import Client

from .config import API_HASH, API_ID, BOT_TOKEN, HELLBOT_SESSION


hellbot = Client("HellBot Music", API_ID, API_HASH, bot_token=BOT_TOKEN)
client = Client(HELLBOT_SESSION, API_ID, API_HASH)

run = client.run
