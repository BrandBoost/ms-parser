from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks
from app.services.parser import create_excel_file, delete_file

api_router = APIRouter()


@api_router.post("/create_excel", status_code=200)
async def get_avito_data(base_id: str, background_tasks: BackgroundTasks):
    excel_file_path, file_name = await create_excel_file(base_id)
    background_tasks.add_task(delete_file, excel_file_path)
    return FileResponse(path=excel_file_path, filename=file_name + ".xlsx")
