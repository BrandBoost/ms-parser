import os
from datetime import datetime
from typing import Optional

from bson import ObjectId
from fastapi import HTTPException

from app.enums.parsers import ParserType
from app.repositories.user_parsers import UserParsersRepository
from app.services.excel import create_excel


async def create_base(parser) -> dict:
    return await UserParsersRepository().create(instance=parser.dict())


async def delete_parser_by_type(parser_type: str, owner_id: str, from_created_at: Optional[datetime],
                                to_created_at: Optional[datetime]) -> list:
    parser = await UserParsersRepository().delete_by_type(parser_type=parser_type, owner_id=owner_id,
                                                          from_created_at=from_created_at,
                                                          to_created_at=to_created_at)
    if not parser:
        raise HTTPException(status_code=404, detail='There are no chosen database with this type')
    return parser


async def get_parser_by_id(parser_id: str, owner_id: str) -> dict:
    parser = await UserParsersRepository().get_by_filter(_id=parser_id, owner_id=owner_id)
    if not parser:
        raise HTTPException(status_code=404, detail='There are no chosen database with this id')
    return parser


async def get_parsers_by_user(user_id: str):
    return await UserParsersRepository().get_by_owner_id(owner_id=user_id)


async def get_all():
    return await UserParsersRepository().get_all()


async def get_all_by_base(base: str):
    return await UserParsersRepository().get_all_by_type(base)


async def get_all_by_status(status: str):
    return await UserParsersRepository().get_all_by_status(status)


# async def delete_by_id(parser_id: str, owner_id: str):
#     parser = await UserParsersRepository().delete_by_id(_id=parser_id, owner_id=owner_id)
#     if not parser:
#         raise HTTPException(status_code=404, detail='There are no chosen database with this id')
#     return parser


async def create_excel_file(base_id: str):
    base = await UserParsersRepository().get_by_id(_id=ObjectId(base_id))
    data = base.get("parser_data")
    if base.get("parser_type") == ParserType.avito.value:
        file_name = ParserType.avito.value
        excel_file = await create_excel(data, file_name)  # type: ignore
        return excel_file, file_name
    elif base.get("parser_type") == ParserType.avito.yandex:
        file_name = ParserType.yandex.value
        excel_file = await create_excel(data, file_name)  # type: ignore
        return excel_file, file_name
    elif base.get("parser_type") == ParserType.vk_groups.value:
        file_name = ParserType.vk_groups.value
        excel_file = await create_excel(data, file_name)  # type: ignore
        return excel_file, file_name
    elif base.get("parser_type") == ParserType.vk_posts.value:
        file_name = ParserType.vk_posts.value
        excel_file = await create_excel(data, file_name)  # type: ignore
        return excel_file, file_name


async def delete_file(file_path: str):
    os.remove(file_path)
