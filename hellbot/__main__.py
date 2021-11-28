import asyncio
import glob
import logging
from pathlib import Path
from pyrogram import idle

from . import hellbot, run, load_plugins


path = "hellbot/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))

async def main():
    await hellbot.start()
    run()
    print("!!! HellBot Music Start-up Complete !!!")
    await hellbot.send_message(LOGGER_ID, "#START \n\nBot is now working")
    await idle()
    await hellbot.stop()


asyncio.get_event_loop().run_until_complete(main())
