from pyrogram import Client

from .config import API_ID, API_HASH, BOT_TOKEN, HELLBOT_SESSION, SUDO_USERS


hellbot = Client(":memory:", API_ID, API_HASH, bot_token=BOT_TOKEN, plugins=dict(root="plugins"))

client = Client(HELLBOT_SESSION, API_ID, API_HASH)
run = client.run

print("!!! HellBot Music Start-up Complete !!!")

hellbot.start()
run()
