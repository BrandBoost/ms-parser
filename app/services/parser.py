from datetime import datetime
from typing import Optional

from fastapi import HTTPException

from app.repositories.user_parsers import UserParsersRepository


async def create_base(parser) -> dict:
    return await UserParsersRepository().create(instance=parser.dict())


async def delete_parser_by_type(parser_type: str, owner_id: str, from_created_at: Optional[datetime],
                                to_created_at: Optional[datetime]) -> list:
    parser = await UserParsersRepository().delet_by_type(parser_type=parser_type, owner_id=owner_id,
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


async def delete_by_id(parser_id: str, owner_id: str):
    return await UserParsersRepository().delete_by_id(_id=parser_id, owner_id=owner_id)


async def delete_all(parser_ids: list, owner_id: str):
    if not parser_ids:
        raise HTTPException(status_code=400, detail="No parser IDs provided")
    return await UserParsersRepository().bulk_delete(ids=parser_ids, owner_id=owner_id)


async def delete_all(owner_id: str):
    if not owner_id:
        raise HTTPException(status_code=400, detail="No user ID provided")

    repository = UserParsersRepository()
    deleted_count = await repository.delete_by_owner_id(owner_id)

    return {"deleted_count": deleted_count}