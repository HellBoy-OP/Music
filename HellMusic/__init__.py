from HellMusic.core.voice import HellVoice
from HellMusic.core.database import HellMongoDB
from HellMusic.core.bot import MusicBot, MusicClient


bot = MusicBot()
client = MusicClient()
hell = HellVoice()
helldb = HellMongoDB().get_db
get_collections = HellMongoDB().get_collections
