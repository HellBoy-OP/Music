import glob
import logging
from pathlib import Path

from . import hellbot, run, load_plugins

hellbot.start()
run()

print("!!! HellBot Music Start-up Complete !!!")
from .plugins import admins, callbacks, chataction, groups, inline, ownercb, owners, play, start, youtube
