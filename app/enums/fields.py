from app.enums.base_enum import BaseEnum


class AvitoFieldOption(BaseEnum):
    item_url = "item_url"
    user_name = "user_name"
    item_title = "item_title"
    price = "price"
    location = "location"
    category = "category"
    created_at = "created_at"
    number_of_views = "number_of_views"
    description = "description"


class VKGroupFields(BaseEnum):
    id = "id"
    group_description = "group_description"
    group_screen_name = "group_screen_name"
    members_count = "members_count"
    group_articles_number = "group_articles_number"
    group_videos_number = "group_videos_number"
    group_country = "group_country"


class VKPostFields(BaseEnum):
    number_of_comments = "number_of_comments"
    post_likes = "post_likes"
    post_text = "post_text"
    owner_id = "owner_id"
    post_reposts = "post_reposts"
    post_views = "post_views"
    crated_at = "crated_at"
