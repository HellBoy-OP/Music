import glob
import logging
from pathlib import Path

from . import hellbot, client, run, load_plugins

hellbot.start()
client.run()
run()

print("!!! HellBot Music Start-up Complete !!!")

