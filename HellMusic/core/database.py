from motor.core import AgnosticCollection
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

from config import Config


class HellMongoDB():
    def __init__(self):
        DB_URI = Config.DB_URI

    async def get_db(self):
        mongo_client = MongoClient(self.DB_URI)
        db = mongo_client.HellMusic
        return db

    def get_collections(self, name: str) -> AgnosticCollection:
        return db[name]
