from unittest import mock

import pytest

from app.schemas.yandex import YandexApiOrganization, OrganizationSearchQuery
from app.tests.conftest import async_client, access_token_with_id


@mock.patch("app.services.yandex.get_all_organizations")
@pytest.mark.asyncio
async def test_retrieve_yandex_organizations(mock_send_yandex_request, async_client, access_token_with_id):
    search_data = {
        "cities": ["Moscow"],
        "categories": ["Automotive"],
        "phones": True,
        "only_mobile_phones": False,
        "without_departments": False,
    }
    organization_data = {
        "parser_type": "Yandex",
        "owner_id": "1",
        "status": "Parsed",
        "parser_data": [
            {
                "coordinates": [
                    24.467465,
                    52.560989
                ],
                "address": "Брестская область, Пружаны, Октябрьская улица, 45А",
                "name": "Сан-Ремо",
                "categories": [
                    {
                        "class": "cafe",
                        "name": "Кафе"
                    }
                ],
                "phone": "+375 29 222-45-39",
                "description": "Октябрьская ул., 45А, Пружаны, Беларусь"
            },
        ],
        "filters": [
            [
                "Пружаны"
            ]
        ],
        "_id": "64af20130b65dcae2979b290"
    }
    mock_send_yandex_request.return_value = organization_data
    response = await async_client.post(
        "api/v1/parsers/yandex/get_organizations", json=search_data, headers=access_token_with_id
    )
    assert response.status_code == 200
