import asyncio
import glob
import logging
from pathlib import Path
from pyrogram import idle

from . import hellbot, run, load_plugins


print("!!! HellBot Music Start-up Complete !!!")

"""
path = "hellbot/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))
"""

hellbot.start()
run()

"""
async def process():
    await hellbot.send_message(LOGGER_ID, "#START \n\nBot is now working")

asyncio.get_event_loop().run_until_complete(process())
"""
