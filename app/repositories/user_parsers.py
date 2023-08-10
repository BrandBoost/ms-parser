from datetime import datetime
from typing import List, Optional

from bson import ObjectId, errors

from app.repositories.base import BaseRepository
from app.schemas.parser import BaseParsersSchema


class UserParsersRepository(BaseRepository):
    def __init__(self):
        self.collection = 'parsers'
        super().__init__()

    async def get_by_id(self, _id: ObjectId):
        # type: ignore
        return await self.db[str(self.collection)].find_one({"_id": _id})

    async def get_by_name(self, name: str):
        # type: ignore
        return await self.db[str(self.collection)].find_one({"name": name})

    async def get_by_owner_id(self, owner_id: str):
        # type: ignore
        return await self.db[str(self.collection)].find({"owner_id": owner_id}).to_list(length=None)

    async def get_all_by_type(self, parser_type: str) -> List[BaseParsersSchema]:
        # type: ignore
        return await self.db[str(self.collection)].find({"parser_type": parser_type}).to_list(length=None)

    async def get_by_filter(self, owner_id: str, _id: str):
        try:
            # type: ignore
            return await self.db[str(self.collection)].find_one({"owner_id": owner_id, "_id": ObjectId(_id)})
        except errors.InvalidId:
            return None

    async def delet_by_type(self, owner_id: str, parser_type: str, from_created_at: Optional[datetime],
                            to_created_at: Optional[datetime]):
        try:
            try:
                query = {"owner_id": owner_id, "parser_type": parser_type}
                if from_created_at is not None:
                    query["created_at"] = {
                        "$gte": from_created_at}  # type: ignore
                if to_created_at is not None:
                    query["created_at"] = {
                        "$lte": to_created_at}  # type: ignore

                # type: ignore
                return await self.db[str(self.collection)].delete_many(query)
            except errors.InvalidId:
                return None
        except errors.InvalidId:
            return None

    async def get_all_by_status(self, status: str) -> List[BaseParsersSchema]:
        # type: ignore
        return await self.db[str(self.collection)].find({"status": status}).to_list(length=None)

    async def delete_by_owner_id(self, owner_id: str):
        try:
            result = await self.db[str(self.collection)].delete_many({"owner_id": owner_id})
            return result.deleted_count
        except errors.InvalidId:
            return 0
