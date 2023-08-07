import typing as tp
from pydantic import BaseModel

from app.enums.parsers import ParserTypeRuss, ParserType


class ParserTypeData(BaseModel):
    label: ParserTypeRuss
    value: ParserType


class ParserTypeFilters(BaseModel):
    region: tp.List[ParserTypeData] = [
        ParserTypeData(label=region_russian, value=region)
        for region, region_russian in zip(ParserType, ParserTypeRuss)
    ]
