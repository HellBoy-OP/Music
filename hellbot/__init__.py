import sys
import logging
import importlib

from pathlib import Path
from pyrogram import Client

from .config import API_HASH, API_ID, BOT_TOKEN, HELLBOT_SESSION


hellbot = Client("HellBot_Music", API_ID, API_HASH, bot_token=BOT_TOKEN) #, plugins=dict(root="plugins"))
client = Client(HELLBOT_SESSION, API_ID, API_HASH)


def load_plugins(plugin_name):
    path = Path(f"hellbot/plugins/{plugin_name}.py")
    name = "hellbot.plugins.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules["hellbot.plugins." + plugin_name] = load
    print(f"🎶 Successfully Imported {plugin_name}")


run = client.run
