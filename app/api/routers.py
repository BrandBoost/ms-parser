from fastapi import APIRouter

from app.api.v1.avito import api_router as avito_api_router
from app.api.v1.vk import api_router as vk_router
from app.api.v1.yandex import api_router as yandex_api_router
from app.api.v1.excel import api_router as excel_api_router
from app.api.v1.parsers import api_router as parser_api_router

v1_router = APIRouter(prefix="/api/v1/parsers")

v1_router.include_router(avito_api_router, prefix="/avito", tags=["avito"])
v1_router.include_router(vk_router, prefix="/vk", tags=["vk"])
v1_router.include_router(yandex_api_router, prefix="/yandex", tags=["yandex"])
v1_router.include_router(excel_api_router, prefix="/excel", tags=["excel"])
v1_router.include_router(parser_api_router, prefix="", tags=["databases"])
