from fastapi import APIRouter, Request

from app.schemas.parser import ReadParsersSchema
from app.services.vk import get_all_groups_parser, get_all_posts_parser
from app.schemas.vk import VKPostsData, VKGroupsData

api_router = APIRouter()


@api_router.post("/get_groups", status_code=200, response_model=ReadParsersSchema)
async def get_groups(request: Request, body: VKGroupsData, count: int):
    fields = body.fields
    user_id = request.state.user_id
    all_data = await get_all_groups_parser(count, fields, user_id)
    return all_data


@api_router.post("/get_posts", status_code=200, response_model=ReadParsersSchema)
async def get_posts(
    request: Request, body: VKPostsData, count: int, group_screen_name: str
):
    fields = body.fields
    user_id = request.state.user_id
    all_data = await get_all_posts_parser(count, group_screen_name, fields, user_id)
    return all_data
