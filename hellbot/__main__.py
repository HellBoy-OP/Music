from pyrogram import Client as Bot

from . import client, run
from .config import API_HASH, API_ID, BOT_TOKEN


Bot(
    'HellBot-Music',
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins={'root': 'hellbot.plugins'},
).start()

run()
client.start()
