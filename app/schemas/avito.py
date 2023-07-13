from typing import Set, Optional

import typing as tp
from pydantic import BaseModel, root_validator

from app.enums.category import AvitoCategory, AvitoCategoryRussian
from app.enums.fields import AvitoFieldOption
from app.enums.limits import Limits
from app.enums.region import AvitoRegionRussian, AvitoRegion


class AvitoFields(BaseModel):
    item_url: Optional[str]
    user_name: Optional[str]
    item_title: Optional[str]
    price: Optional[str]
    location: Optional[str]
    category: Optional[str]
    created_at: Optional[str]
    number_of_views: Optional[str]
    description: Optional[str]

    @root_validator(pre=True)
    def parse_raw_object(cls, values: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
        values["item_url"] = values["item_url"]
        values["user_name"] = values["user_name"]
        values["item_title"] = values["item_title"]
        values["price"] = values["price"]
        values["location"] = values["location"]
        values["category"] = values["category"]
        values["created_at"] = values["created_at"]
        values["number_of_views"] = values["number_of_views"]
        values["description"] = values["description"]

        return values

    def to_dict(self):
        return self.dict()


class AvitoRegionDataItem(BaseModel):
    label: AvitoRegionRussian
    value: AvitoRegion


class AvitoCategoryDataItem(BaseModel):
    label: AvitoCategoryRussian
    value: AvitoCategory


class AvitoParserData(BaseModel):
    fields: Set[AvitoFieldOption] = set(AvitoFieldOption)


class AvitoFilters(BaseModel):
    region: tp.List[AvitoRegionDataItem] = [
        {"label": region_russian, "value": region}  # type: ignore
        for region, region_russian in zip(AvitoRegion, AvitoRegionRussian)
    ]
    category: tp.List[AvitoCategoryDataItem] = [
        {"label": category_russian, "value": category}  # type: ignore
        for category, category_russian in zip(AvitoCategory, AvitoCategoryRussian)
    ]
    limits: tp.Set[Limits] = set(Limits)
