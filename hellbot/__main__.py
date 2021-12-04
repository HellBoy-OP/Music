import asyncio

from pyrogram import idle

from . import hellbot, client


# Starting HellBot Music
async def startup():
    print("••• HellBot Music Starting •••")
    await client.start()
    await hellbot.start()
    print("••• HellBot Music Started •••")
    await idle()


loop = asyncio.get_event_loop()
if __name__ == "__main__":
    loop.run_until_complete(startup())
