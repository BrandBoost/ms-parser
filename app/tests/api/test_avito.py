from unittest.mock import patch

import mock
import pytest

from app.tests.conftest import async_client, access_token_with_id
from httpx import AsyncClient


@pytest.mark.asyncio
class TestOrder:
    @mock.patch('app.parsers.avito.avito_driver.AvitoDriver.initialize')
    @mock.patch('app.parsers.avito.avito_driver.AvitoDriver.quit')
    @pytest.mark.asyncio
    async def test_parser_avito_get_all_data(self, mock_quit, mock_initialize, async_client: AsyncClient,
                                             access_token_with_id):
        with patch('app.parsers.avito.avito_parser.AvitoParser.get_all_data') as get_all_data_mock:
            mock_initialize.return_value = None
            mock_quit.return_value = None
            get_all_data_mock.return_value = [
                {"item_title": "Item 1"},
                {"item_title": "Item 2"},
            ]

            payload = {"fields": ["item_title", "price", "created_at"]}
            response = await async_client.post(
                "/api/v1/parsers/avito/get_data?region=all&category=transport&limit=2",
                json=payload,
                headers=access_token_with_id
            )

            assert response.status_code == 200
            get_all_data_mock.assert_called_once()
