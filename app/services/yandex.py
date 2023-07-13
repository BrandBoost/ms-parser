import asyncio

from aiohttp import ClientSession

from app.config import settings
from app.enums.parsers import ParserStatus, ParserType
from app.schemas.parser import BaseParsersSchema
from app.schemas.yandex import YandexApiOrganization
from app.schemas.yandex import OrganizationSearchQuery
from app.services import parser

organization_url: str = settings.ORGANIZATION_URL  # type: ignore
geocoder_url: str = settings.GEOCODER_URL  # type: ignore


# todo: add description for yandex api in Readme.md
async def get_coordinates(city: str):
    """
    Receives the name of a city and returns its coordinates (latitude and longitude).

    :param city: The name of the city (e.g., Minsk, Moscow, etc.).
    :return: A tuple of latitude and longitude (latitude, longitude).
    """

    url = geocoder_url + f"&format=json&geocode={city}"
    async with ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            feature_member = data["response"]["GeoObjectCollection"]["featureMember"][0]
            point = feature_member["GeoObject"]["Point"]["pos"]
            longitude, latitude = map(float, point.split())
            return latitude, longitude


async def fetch_data(session: ClientSession, url: str):
    async with session.get(url) as response:
        return await response.json()


async def get_all_organizations(data: OrganizationSearchQuery, user_id):
    tasks = []

    async with ClientSession() as session:
        for city in data.cities:
            latitude, longitude = await get_coordinates(city)
            for category in data.categories:
                params = f"&text={category}&ll={longitude},{latitude}&spn=0.1,0.1&lang=ru_RU&type=biz&results=500"
                url = (organization_url + params)
                tasks.append(fetch_data(session, url))

        responses = await asyncio.gather(*tasks)
        organizations = []

        for response in responses:
            for feature in response["features"]:
                properties = feature["properties"]

                # Фильтр по телефонам
                if data.phones and not properties["CompanyMetaData"].get(
                        "Phones", None
                ):
                    continue

                # Фильтр по мобильным телефонам
                if data.only_mobile_phones and not properties["CompanyMetaData"].get(
                        "Phones", None
                ):
                    phones = properties["Phones"]
                    if not any(phone.get("type") == "phone_mobile" for phone in phones):
                        continue

                # Фильтр по филиалам
                if data.without_departments and properties.get("CompanyMetaData", None):
                    company_data = properties["CompanyMetaData"]
                    if "branch_count" in company_data and company_data["branch_count"] > 0:
                        continue

                # Отфильтровать только нужные поля
                organization_data = {
                    "coordinates": feature["geometry"]["coordinates"],
                    "address": properties["CompanyMetaData"]["address"],
                    "name": properties["CompanyMetaData"]["name"],
                    "categories": properties["CompanyMetaData"]["Categories"],
                    "phone": properties["CompanyMetaData"]
                    .get("Phones", [{}])[0]
                    .get("formatted"),
                    "description": properties.get("description"),
                }
                organizations.append(YandexApiOrganization(**organization_data))
        parser_data = BaseParsersSchema(
            parser_type=ParserType.yandex,
            owner_id=user_id,
            status=ParserStatus.parsed,
            parser_data=organizations,
            filters=[data.categories, data.cities]
        )
        user_parser = await parser.create_base(parser_data)
        return user_parser
