from typing import Set, Optional, Union

import typing as tp
from pydantic import BaseModel, root_validator, Extra

from app.enums.fields import VKPostFields, VKGroupFields


class VKGroupsParserFields(BaseModel):
    id: Optional[str]
    group_description: Optional[str]
    group_screen_name: Optional[str]
    members_count: Optional[str]
    group_articles_number: Optional[Union[int, dict, str]]
    group_videos_number: Optional[Union[int, dict, str]]
    group_country: Optional[str]

    class Config:
        extra = Extra.ignore

    @root_validator(pre=True)
    def parse_raw_object(cls, values: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
        values["id"] = values["id"]
        values["group_description"] = values["group_description"]
        values["group_screen_name"] = values["group_screen_name"]
        values["members_count"] = values["members_count"]
        values["group_articles_number"] = values["group_articles_number"]
        values["group_videos_number"] = values["group_videos_number"]
        values["group_country"] = values["group_country"]

        return values

    def to_dict(self):
        return self.dict()


class VKPostsParserFields(BaseModel):
    number_of_comments: Optional[str]
    post_likes: Optional[str]
    post_text: Optional[str]
    owner_id: Optional[str]
    post_reposts: Optional[str]
    post_views: Optional[str]
    crated_at: Optional[str]

    class Config:
        extra = Extra.ignore

    @root_validator(pre=True)
    def parse_raw_object(cls, values: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
        values["number_of_comments"] = values["number_of_comments"]
        values["post_likes"] = values["post_likes"]
        values["post_text"] = values["post_text"]
        values["post_reposts"] = values["post_reposts"]
        values["post_views"] = values["post_views"]
        values["crated_at"] = values["crated_at"]

        return values

    def to_dict(self):
        return self.dict()


class VKGroupsData(BaseModel):
    fields: Set[VKGroupFields] = set(VKGroupFields)


class VKPostsData(BaseModel):
    fields: Set[VKPostFields] = set(VKPostFields)
