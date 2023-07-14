import typing as tp

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.database.mongo import MongoManager


class BaseRepository(MongoManager):
    collection: AsyncIOMotorCollection = None  # type: ignore

    def __init__(self):
        super().__init__()

    async def get_all(self):
        await self.get_db()
        return await self.db[self.collection].find().to_list(length=None)  # type: ignore

    async def create(self, instance: dict) -> dict:
        result = await self.db[self.collection].insert_one(instance)  # type: ignore
        created_instance = await self.db[self.collection].find_one({"_id": result.inserted_id})  # type: ignore
        return created_instance  # type: ignore

    async def delete_by_id(self, _id: tp.Union[str, ObjectId]) -> None:
        user_id = ObjectId(_id) if isinstance(_id, str) else _id
        await self.db[self.collection].delete_one({'_id': user_id})
