from app.parsers.avito.avito_parser import AvitoParser
from app.schemas.parser import BaseParsersSchema
from app.services import parser
from app.enums.parsers import ParserType, ParserStatus


async def get_all(fields, region, category, user_id, limit):
    parser_avito = AvitoParser()
    await parser_avito.avito_driver.initialize()
    data = await parser_avito.get_all_data(fields, region, category, limit)
    await parser_avito.avito_driver.quit()
    parser_data = BaseParsersSchema(
        parser_type=ParserType.avito,
        owner_id=user_id,
        status=ParserStatus.parsed,
        parser_data=list(data),
        filters=list(fields),
    )
    user_parser = await parser.create_base(parser_data)
    return user_parser
