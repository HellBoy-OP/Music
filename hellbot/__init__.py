from aiohttp import ClientSession
from pyrogram import Client
from Python_ARQ import ARQ

from .config import API_HASH, API_ID, ARQ_API_URL, ARQ_API_KEY, BOT_TOKEN, HELLBOT_SESSION


hellbot = Client("HellBot_Music", API_ID, API_HASH, bot_token=BOT_TOKEN, plugins=dict(root="plugins"))
client = Client(HELLBOT_SESSION, API_ID, API_HASH)
aiosession = ClientSession()
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiosession)


run = client.run
