import sys
import asyncio
from config import Config
from pyrogram import idle
from HellMusic.core.logging import LOGS
from HellMusic.helpers.text import DEPLOYED
from HellMusic.core.plugins import load_plugins
from HellMusic import bot, hell, client, helldb, __version__


loop = asyncio.get_event_loop()


async def startup():
    if not Config.HELLBOT_SESSION:
        LOGS.error("[HELLBOT_SESSION]: Not a valid session!")
        sys.exit()

    LOGS.info("••• Music Bot Startup •••")

    await bot.start()
    await client.start()
    await hell.start()
    await load_plugins()

    if Config.DB_URI:
        LOGS.info("••• Database Url Found •••")
        await helldb.get_db()

    LOGS.info(DEPLOYED.format(__version__.version))
    await idle()


if __name__ == "__main__":
    loop.run_until_complete(startup())
    LOGS.info("••• Hell-Music Stopped •••")
