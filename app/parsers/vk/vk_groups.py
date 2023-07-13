import asyncio
from typing import List

import aiohttp

# TODO we have to separate services or rename structure
from app.config.settings import VK_ACCESS_TOKEN, logger  # type: ignore
from app.schemas.vk import VKGroupsParserFields

payload = {
    "access_token": VK_ACCESS_TOKEN,
    "v": "5.81",
}


async def fetch_groups(session, count, offset):
    payload["count"] = count
    payload["offset"] = offset
    async with session.get(
        "https://api.vk.com/method/groups.get", params=payload
    ) as response:
        data = await response.json()
        return data["response"]["items"]


async def get_all_groups(count):
    offset = 0
    all_groups = []
    async with aiohttp.ClientSession() as session:
        while offset < count:
            data = await fetch_groups(session, count, offset)
            for group_id in data:
                payload["group_id"] = group_id
                payload[
                    "fields"
                ] = "status, members_count, description, country, counters"
                async with session.get(
                    "https://api.vk.com/method/groups.getById", params=payload
                ) as response:
                    await asyncio.sleep(1)
                    groups_data = await response.json()
                    all_groups.append(groups_data["response"][0])
            offset += 100
    return all_groups


async def get_item(item: str, group, sub_item=None):
    try:
        elem = group[item]
        if sub_item is not None and isinstance(elem, dict) and sub_item in elem:
            return elem[sub_item]
        else:
            return "Элемент отсутствует" if elem is None else elem
    except Exception as ex:
        logger.debug(ex)
        return "Элемент отсутствует"


async def get_groups_data(count, fields_to_parse: List[str]) -> list:
    get_all_data = []
    groups = await get_all_groups(count)
    for group in groups:
        post_data = VKGroupsParserFields(
            id=await get_item("id", group) if "id" in fields_to_parse else None,
            group_description=await get_item("description", group)
            if "group_description" in fields_to_parse
            else None,
            group_screen_name=await get_item("screen_name", group)
            if "group_screen_name" in fields_to_parse
            else None,
            members_count=await get_item("members_count", group)
            if "members_count" in fields_to_parse
            else None,
            group_articles_number=await get_item("counters", group, "articles")
            if "group_articles_number" in fields_to_parse
            else None,
            group_videos_number=await get_item("counters", group, "videos")
            if "group_videos_number" in fields_to_parse
            else None,
            group_country=await get_item("country", group, "title")
            if "group_country" in fields_to_parse
            else None,
        )
        get_all_data.append(post_data)
    filtered_data = [
        {field: getattr(data, field) for field in fields_to_parse}
        for data in get_all_data
    ]
    return filtered_data
