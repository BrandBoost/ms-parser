from unittest.mock import patch

import mock
import pytest

from app.tests.conftest import async_client, access_token_with_id


@pytest.mark.asyncio
async def test_retrieve_user_parsers(async_client, access_token_with_id, global_dict):
    response = await async_client.get(
        url=f'/api/v1/parsers/retrieve_user_parsers/',
        headers=access_token_with_id
    )
    global_dict["parser_id"] = response.json()[0]["_id"]
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_excel(async_client, access_token_with_id, global_dict):
    response = await async_client.post(
        url=f'/api/v1/parsers/excel/create_excel?base_id={global_dict["parser_id"]}',
        headers=access_token_with_id
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_retrieve_user_parser(async_client, access_token_with_id, global_dict):
    response = await async_client.get(
        url=f'/api/v1/parsers/retrieve_user_parsers/{global_dict["parser_id"]}/',
        headers=access_token_with_id
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_parser(async_client, access_token_with_id, global_dict):
    response = await async_client.delete(
        url=f'/api/v1/parsers/delete_user_parser_by_id/{global_dict["parser_id"]}/',
        headers=access_token_with_id
    )
    assert response.status_code == 200
