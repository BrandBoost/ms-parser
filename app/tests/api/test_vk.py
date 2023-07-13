from unittest.mock import patch
import pytest

from httpx import AsyncClient
from app.tests.conftest import async_client, access_token_with_id


@pytest.mark.asyncio
async def test_parser_vk_get_groups(async_client: AsyncClient, access_token_with_id):
    with patch("app.parsers.vk.vk_groups.get_all_groups") as get_all_groups_mock:
        get_all_groups_mock.return_value = [
            {"group_videos_number": "2"},
            {"id": "144329953"},
        ]

        payload = {"fields": ["group_videos_number", "id"]}
        response = await async_client.post(
            "api/v1/parsers/vk/get_groups?count=10", json=payload,
            headers=access_token_with_id
        )

        assert response.status_code == 200
        get_all_groups_mock.assert_called_once()


@pytest.mark.asyncio
async def test_parser_vk_get_posts(async_client: AsyncClient, access_token_with_id):
    with patch("app.parsers.vk.vk_posts.fetch_posts") as get_all_posts_mock:

        payload = {"fields": ["post_text"]}
        response = await async_client.post(
            "/api/v1/parsers/vk/get_posts?count=100&group_screen_name=hero_blog",
            json=payload,
            headers=access_token_with_id
        )

        assert response.status_code == 200
        get_all_posts_mock.assert_called_once()
