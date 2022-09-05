import glob
import importlib
import sys
from pathlib import Path

from HellMusic.core.logging import LOGS


def _plugins(plugin_name):
    path = Path(f"HellMusic/plugins/{plugin_name}.py")
    name = "HellMusic.plugins.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules["HellMusic.plugins." + plugin_name] = load
    LOGS.info(f"[Imported]: {plugin_name}")


async def load_plugins():
    path = "HellMusic/plugins/*.py"
    files = glob.glob(path)
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem
            _plugins(plugin_name.replace(".py", ""))
