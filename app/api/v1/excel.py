from fastapi import APIRouter, UploadFile, Request, Body
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks

from app.enums.parsers import ParserType
from app.schemas.excel import ParserTypeFilters
from app.schemas.parser import GetListParserData
from app.services.excel import create_excel_file, delete_file, import_excel

api_router = APIRouter()


@api_router.post("/create_excel", status_code=200)
async def get_avito_data(base_id: str, background_tasks: BackgroundTasks):
    excel_file_path, file_name = await create_excel_file(base_id)
    background_tasks.add_task(delete_file, excel_file_path)
    return FileResponse(path=excel_file_path, filename=file_name + ".xlsx")


@api_router.post("/import_parser/", status_code=200, response_model=GetListParserData)
async def import_parser(request: Request, excel_file: UploadFile,
                        parser_type: ParserType = Body(), filters: list[str] = Body()):
    user_id = request.state.user_id
    excel_file = await import_excel(user_id, excel_file.file, parser_type, filters)
    return excel_file


@api_router.get("/get_excel_types/", status_code=200)
async def get_excel_types() -> ParserTypeFilters:
    response_model = ParserTypeFilters()
    return response_model
