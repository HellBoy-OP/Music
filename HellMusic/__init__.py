from HellMusic.core.voice import HellVoice
from HellMusic.core.database import HellMongoDB
from HellMusic.core.bot import MusicBot, MusicClient
from config import Config

bot = MusicBot()
client = MusicClient()
hell = HellVoice()
helldb = HellMongoDB()
trg = Config.TRIGGERS
