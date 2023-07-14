import io

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
async def test_excel_filters(async_client, access_token_with_id):
    response = await async_client.get(
        url=f'/api/v1/parsers/excel/get_excel_types/',
        headers=access_token_with_id
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_excel_import(async_client, access_token_with_id):
    file_obj = io.BytesIO(b"test file content")
    file_obj.name = "test_file.xlsx"
    filters = ["string", "string2", "string3", "string4"]
    response = await async_client.post(
        url=f'/api/v1/parsers/excel/import_parser/?parser_type=Avito',
        files={"excel_file": file_obj},
        data=filters,
        headers=access_token_with_id
    )
    assert response.status_code == 200
