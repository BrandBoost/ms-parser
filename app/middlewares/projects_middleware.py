from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException

from app.config import settings


async def get_projects(request: Request):
    user_id = request.state.user_id
    collection_name = "users"

    client = AsyncIOMotorClient(settings.MONGO_URI)

    async with await client.start_session() as session:
        async with session.start_transaction():
            db = client[str(settings.DB_NAME)]
            projects = await db[collection_name].find_one({"_id": ObjectId(user_id)}, {"projects": 1})
    client.close()

    return projects["projects"]


class ProjectsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        projects = await get_projects(request)

        if not projects:
            raise HTTPException(status_code=403, detail="You don't have any projects or Create a new one!")

        request.state.projects = projects

        response = await call_next(request)
        return response
