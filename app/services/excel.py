import openpyxl
import pandas as pd


async def get_headers(keys, header_row: int, sheet):
    for col, key in enumerate(keys, start=1):
        sheet.cell(row=header_row, column=col, value=key)


async def get_keys(data):
    keys = set()

    for d in data:
        key_set = d.keys()
        keys = keys.union(key_set)
    return keys


async def create_excel(data: list, name_of_excel: str) -> str:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    keys = await get_keys(data)
    await get_headers(keys, 1, sheet)
    for row, obj in enumerate(data, start=1 + 1):
        for col, key in enumerate(keys, start=1):
            value = str(obj.get(key))
            sheet.cell(row=row, column=col, value=value)  # type: ignore
    excel_file = f"{name_of_excel}.xlsx"
    workbook.save(excel_file)
    return excel_file


def read_headers():
    data_frame = pd.read_excel('D:\Projects\PycharmProjects\Test.xlsx')
    headers = data_frame.columns.tolist()
    return headers, data_frame


def read_excel(headers, data_frame):
    row = 0
    first_row_values = {}
    result = []
    while row is not None:
        try:
            for header in headers:
                first_row_values[header] = data_frame[header].iloc[row]
            row += 1
            result.append(first_row_values)
            print(result)
        except IndexError:
            break
    return result


headers, data_frame = read_headers()
print(read_excel(headers, data_frame))
