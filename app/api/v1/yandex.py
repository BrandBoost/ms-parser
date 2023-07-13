
from fastapi import APIRouter, Request

from app.schemas.parser import ReadParsersSchema
from app.schemas.yandex import OrganizationSearchQuery
from app.services import yandex

api_router = APIRouter()


@api_router.post("/get_organizations", status_code=200, response_model=ReadParsersSchema)
async def retrieve_yandex_organizations(request: Request, search_data: OrganizationSearchQuery):
    user_id = "1"
    user_data = await yandex.get_all_organizations(search_data, user_id)
    print(user_data)
    return await yandex.get_all_organizations(search_data, user_id)
