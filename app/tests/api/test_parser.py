import io

import pytest
import mock

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
async def test_get_parser_ids(async_client, access_token_with_id):
    response = await async_client.get(
        url=f'/api/v1/parsers/excel/get_parser_ids/',
        headers=access_token_with_id
    )
    assert response.status_code == 200


@mock.patch('app.services.excel.read_excel')
@mock.patch('app.services.excel.read_headers')
@pytest.mark.asyncio
async def test_excel_import(mock_read_headers, mock_read_excel, async_client, access_token_with_id):
    mock_read_headers.return_value = ['header1', 'header2']
    mock_read_excel.return_value = [
        {"header1": "value1_row1", "header2": "value2_row1"},
        {"header1": "value1_row2", "header2": "value2_row2"},
    ]
    file_obj = io.BytesIO(b"test file content")
    file_obj.name = "test_file.xlsx"
    filters = ["string", "string2", "string3", "string4"]
    response = await async_client.post(
        url=f'/api/v1/parsers/excel/import_parser/',
        files={"excel_file": (
            file_obj.name, file_obj, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        data={"filters": filters, "parser_type": "Avito"},
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


@pytest.mark.asyncio
async def test_get_filters(async_client, access_token_with_id):
    response = await async_client.get(
        url=f'/api/v1/parsers/get_filters/?parser_type=Yandex',
        headers=access_token_with_id
    )
    assert response.status_code == 200
