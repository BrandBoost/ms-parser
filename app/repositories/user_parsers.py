from datetime import datetime
from typing import List, Optional

from bson import ObjectId, errors

from app.repositories.base import BaseRepository
from app.schemas.parser import BaseParsersSchema


class UserParsersRepository(BaseRepository):
    def __init__(self):
        self.collection = 'parsers'
        super().__init__()

    # TODO: Денис, везде возвращем не dict, а схему т.к. у нас репозиторий с парсерами то они должны возварщать оп типу:
    #  -> ReadParsersSchema:
    #  это к первым двум эндпоинтам тут, просто я не знаю какую схему ты планировал возвращать
    async def get_by_id(self, _id: ObjectId) -> dict:
        return await self.db[self.collection].find_one({"_id": _id})  # type: ignore

    async def get_by_name(self, name: str) -> dict:
        return await self.db[self.collection].find_one({"name": name})  # type: ignore

    async def get_by_owner_id(self, owner_id: str):
        return await self.db[self.collection].find({"owner_id": owner_id}).to_list(length=None)  # type: ignore

    async def get_all_by_type(self, parser_type: str) -> List[BaseParsersSchema]:
        return await self.db[self.collection].find({"parser_type": parser_type}).to_list(length=None)  # type: ignore

    async def get_by_filter(self, owner_id: str, _id: str):
        try:
            return await self.db[self.collection].find_one({"owner_id": owner_id, "_id": ObjectId(_id)})  # type: ignore
        except errors.InvalidId:
            return None

    async def delete_by_type(self, owner_id: str, parser_type: str, from_created_at: Optional[datetime],
                             to_created_at: Optional[datetime]):
        try:
            try:
                query = {"owner_id": owner_id, "parser_type": parser_type}
                if from_created_at is not None:
                    query["created_at"] = {"$gte": from_created_at}  # type: ignore
                if to_created_at is not None:
                    query["created_at"] = {"$lte": to_created_at}  # type: ignore

                return await self.db[self.collection].delete_many(query)  # type: ignore
            except errors.InvalidId:
                return None
        except errors.InvalidId:
            return None

    async def get_all_by_status(self, status: str) -> List[BaseParsersSchema]:
        return await self.db[self.collection].find({"status": status}).to_list(length=None)  # type: ignore
