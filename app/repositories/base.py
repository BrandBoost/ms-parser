import logging
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

    async def delete_by_id(self, _id: tp.Union[str, ObjectId], owner_id: str) -> None:
        user_id = ObjectId(_id) if isinstance(_id, str) else _id
        await self.db[str(self.collection)].delete_one({'_id': user_id, "owner_id": owner_id})

    async def bulk_delete(self, ids: tp.List[tp.Union[str, ObjectId]], owner_id) -> None:
        try:
            parser_ids = [ObjectId(parser_id) if isinstance(parser_id, str) else parser_id for parser_id in ids]
            result = await self.db[str(self.collection)].delete_many({'_id': {"$in": parser_ids}, "owner_id": owner_id})
            logging.info("Delete result: %s", result)
        except Exception as e:
            logging.error("Error during delete operation: %s", str(e))
