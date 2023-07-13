from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import PyMongoError
from app.config import logger
from app.config.settings import DB_NAME, MONGO_URI  # type: ignore


class MongoManager:
    client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_URI)
    db: AsyncIOMotorDatabase = client[DB_NAME]  # type: ignore

    @classmethod
    async def connect(cls):
        try:
            logger.info("Connected to MongoDB")
            if cls.db is None:
                cls.db = cls.client[DB_NAME]
            return cls
        except PyMongoError as e:
            logger.info(f"Error connecting to MongoDB: {str(e)}")

    @classmethod
    async def close(cls):
        if cls.client:
            cls.client.close()

    @classmethod
    async def create_indexes(cls):
        # TODO create indexes
        ...

    @classmethod
    async def get_db(cls) -> AsyncIOMotorDatabase:
        return cls.db if cls.db is not None else await cls.connect()
