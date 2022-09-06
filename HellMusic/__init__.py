from config import Config
from HellMusic.core.voice import HellVoice
from HellMusic.core.client import sudo_users
from HellMusic.core.database import HellMongoDB
from HellMusic.core.bot import MusicBot, MusicClient


bot = MusicBot()
client = MusicClient()
hell = HellVoice()
helldb = HellMongoDB()
trg = Config.TRIGGERS
SUDO_USERS = sudo_users()
