import asyncio
import sys

from config import Config
from pyrogram import idle
from HellMusic import bot, hell, client, helldb
from HellMusic.core.logging import LOGS
from HellMusic.core.plugins import load_plugins
from HellMusic.helpers.text import DEPLOYED
from HellMusic import __version__

async def startup():
    if not Config.HELLBOT_SESSION:
        LOGS.error("[HELLBOT_SESSION]: Not a valid session!")
        sys.exit()

    LOGS.info("••• Music Bot Startup •••")

    await bot.start()
    await load_plugins()
    await client.start()
    await hell.start()

    LOGS.info(DEPLOYED.format(__version__.version))
    await idle()
    LOGS.info("••• Hell-Music Stopped •••")


asyncio.run(startup())
