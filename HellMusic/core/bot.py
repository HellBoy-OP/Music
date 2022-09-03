import sys

from pyrogram import Client

from config import Config
from HellMusic.core.logging import LOGS


class MusicBot(Client):
    def __init__(self):
        super().__init__(
            "HellMusic",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
        )

    async def start(self):
        LOGS.info("••• Starting Hell-Music Bot •••")
        await super().start()
        get_bot = await self.get_me()
        self.username = get_bot.username
        self.id = get_bot.id
        try:
            await self.send_message(
                Config.LOGGER_ID,
                "#START #BOT \n\n__Hell-Music Bot Started Successfully !!__",
            )
            self.name = f"{get_bot.first_name} {get_bot.last_name or ''}"
            LOGS.info(f"[{self.name}]: Hell-Music Bot Started Successfully !!")
        except:
            LOGS.error("[LOGGER_ID]: Invalid logger channel found. Please re-check LOGGER_ID !")
            sys.exit()


class MusicClient(Client):
    def __init__(self):
        super().__init__(
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            session_name=str(Config.HELLBOT_SESSSION),
            no_updates=True,
        )

    async def start(self):
        LOGS.info("••• Starting Hell-Music Client •••")
        await super().start()
        get_bot = await self.get_me()
        self.username = get_bot.username
        self.id = get_bot.id
        try:
            await self.join_chat("Its_HellBot")
            await self.join_chat("https://t.me/+bZxlmdNFp1NjMDNh")
        except:
            pass
        try:
            await self.send_message(
                Config.LOGGER_ID,
                "#START #CLIENT \n\n__Hell-Music Client Started Successfully !!__",
            )
            self.name = f"{get_bot.first_name} {get_bot.last_name or ''}"
            LOGS.info(f"[{self.name}]: Hell-Music Bot Started Successfully !!")
        except:
            LOGS.error("[LOGGER_ID]: Invalid logger channel found. Please re-check LOGGER_ID !")
            sys.exit()
