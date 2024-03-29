from config import Config
from motor.core import AgnosticCollection
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient


class HellMongoDB:
    def __init__(self):
        self.DB_URI = Config.DB_URI

    async def get_db(self):
        mongo_client = MongoClient(self.DB_URI)
        db = mongo_client.HellMusic
        return db

    async def get_collections(self, name: str) -> AgnosticCollection:
        db = await self.get_db()
        return db[name]
