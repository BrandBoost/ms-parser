from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.responses import PlainTextResponse

from app.enums.parsers import ParserType
from app.schemas.avito import AvitoFilters
from app.schemas.parser import GetListParserData, GetFilters
from app.schemas.parser import ReadParsersSchema
from app.services import parser

api_router = APIRouter()


@api_router.get("/retrieve_user_parsers/", status_code=200, response_model=List[GetListParserData])
async def list_of_all_pre_parsers_data(request: Request):
    user_id = request.state.user_id
    return await parser.get_parsers_by_user(user_id=user_id)


@api_router.get("/retrieve_user_parsers/{parser_id}/", status_code=200, response_model=ReadParsersSchema)
async def retrieve_all_pre_parsers_data(request: Request, parser_id: str):
    user_id = request.state.user_id
    return await parser.get_parser_by_id(parser_id=parser_id, owner_id=user_id)


@api_router.delete("/delete_user_parsers/", status_code=204)
async def delete_user_parsers(
        request: Request,
        parser_type: str = Query(),
        from_created_at: Optional[datetime] = Query(None),
        to_created_at: Optional[datetime] = Query(None)
):
    user_id = request.state.user_id
    await parser.delete_parser_by_type(parser_type=parser_type, owner_id=user_id, from_created_at=from_created_at,
                                       to_created_at=to_created_at)
    return PlainTextResponse("Deletion completed successfully")


@api_router.delete("/delete_user_parser_by_id/{parser_id}/", status_code=200, response_model=ReadParsersSchema)
async def delete_user_parser_by_id(request: Request, parser_id: str,):
    user_id = request.state.user_id
    await parser.delete_by_id(parser_id=parser_id, owner_id=user_id)
    return PlainTextResponse("Deletion completed successfully")


@api_router.get("/get_filters/", status_code=200)
async def get_filters(parser_type: str):
    if not parser_type:
        raise HTTPException(status_code=400, detail="Parser type not provided")
    elif parser_type == ParserType.avito:
        return AvitoFilters()
    elif parser_type == ParserType.yandex:
        return GetFilters()
    elif parser_type == ParserType.vk_groups:
        return GetFilters()
    elif parser_type == ParserType.vk_posts:
        return GetFilters()
    raise HTTPException(status_code=400, detail="Parser type not provided")
