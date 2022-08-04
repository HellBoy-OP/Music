from Python_ARQ import ARQ
from pyrogram import Client
from aiohttp import ClientSession
from pytgcalls import GroupCallFactory
from .config import (
    API_ID, API_HASH, BOT_TOKEN, ARQ_API_KEY, ARQ_API_URL, HELLBOT_SESSION)


# Bot Client
hellbot = Client(
    "HellBot-Music",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "hellbot.plugins"},
)

# User Client
client = Client(
    HELLBOT_SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins={"root": "hellbot.plugins"},
)

# ARQ Client
aiosession = ClientSession()
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiosession)

# Pytgcalls client
PyCalls = GroupCallFactory(
    client, outgoing_audio_bitrate_kbit=320
).get_file_group_call()
