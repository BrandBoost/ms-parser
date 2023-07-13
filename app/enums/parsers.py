from app.enums.base_enum import BaseEnum


class ParserStatus(BaseEnum):
    in_progress = "In Progress"
    parsed = "Parsed"


class ParserType(BaseEnum):
    yandex = "Yandex"
    avito = "Avito"
    vk_groups = "Vk Groups"
    vk_posts = "Vk Posts"
