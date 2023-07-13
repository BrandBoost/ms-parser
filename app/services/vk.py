
from app.enums.parsers import ParserStatus, ParserType
from app.parsers.vk.vk_groups import get_groups_data
from app.parsers.vk.vk_posts import get_posts_data
from app.schemas.parser import BaseParsersSchema
from app.services import parser


async def get_all_groups_parser(count, fields, user_id):
    data = await get_groups_data(count, fields)
    parser_data = BaseParsersSchema(
        parser_type=ParserType.vk_groups,
        owner_id=user_id,
        status=ParserStatus.parsed,
        parser_data=data,
        filters=list(fields)
    )
    user_parser = await parser.create_base(parser_data)
    return user_parser


async def get_all_posts_parser(count, group_screen_name, fields, user_id):
    data = await get_posts_data(count, group_screen_name, fields)
    parser_data = BaseParsersSchema(
        parser_type=ParserType.vk_posts,
        owner_id=user_id,
        status=ParserStatus.parsed,
        parser_data=data,
        filters=list(fields)
    )
    user_parser = await parser.create_base(parser_data)
    return user_parser
