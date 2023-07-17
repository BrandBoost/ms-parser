from datetime import datetime
from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field

from app.enums.parsers import ParserStatus
from app.schemas.mongo_validators import PyObjectId


class PreRetrieveParsersSchema(BaseModel):
    parser_type: str
    owner_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    status: ParserStatus

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class BaseParsersSchema(PreRetrieveParsersSchema):
    parser_data: List
    filters: List


class GetListParserData(PreRetrieveParsersSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    filters: List


class ReadParsersSchema(BaseParsersSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


class GetFilters(BaseModel):
    pass
