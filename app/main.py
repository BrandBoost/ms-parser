from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import (
    URL_LOCALHOST_FRONT,
    URL_BRENDBOOST_BACK,
    URL_BRENDBOOST_FRONT, logger,
)

from app.api import v1_router
from app.database.mongo import MongoManager
from app.middlewares.auth_middleware import ApiKeyMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[URL_LOCALHOST_FRONT, URL_BRENDBOOST_BACK, URL_BRENDBOOST_FRONT],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ApiKeyMiddleware)


@app.on_event("startup")
async def on_startup():
    await MongoManager.connect()
    logger.info('Startup event - connecting to the database')


app.include_router(v1_router)
