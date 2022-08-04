import asyncio
from pyrogram import idle
from . import client, hellbot
from .config import LOGGER_ID


# Starting HellBot Music
async def startup():
    print("••• HellBot Music Starting •••")
    await client.start()
    await hellbot.start()
    await hellbot.send_message(
        LOGGER_ID, "#START \n\n<b><i>HellBot Music Started Successfully!!</b></i>"
    )
    print("••• HellBot Music Started •••")
    await idle()


loop = asyncio.get_event_loop()
if __name__ == "__main__":
    loop.run_until_complete(startup())
