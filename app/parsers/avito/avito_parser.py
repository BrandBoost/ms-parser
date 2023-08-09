import asyncio
from typing import List

from selenium.common import NoSuchElementException

from app.parsers.avito.avito_driver import AvitoDriver
from app.config.settings import logger
from app.schemas.avito import AvitoFields


class AvitoParser:
    def __init__(self):
        self.avito_driver = AvitoDriver()
        self.item_data = {}
        self.all_data = []

    async def get_items(self, region, category):
        try:
            await self.avito_driver.initialize()
            self.avito_driver.driver.get(
                "https://www.avito.ru/" + region + "/" + category
            )
            await asyncio.sleep(2)
            items = self.avito_driver.driver.find_elements(
                "xpath", "//div[@data-marker='item-photo']"
            )
            return items
        except Exception as ex:
            logger.debug(f"No such element. {ex} ")

    async def get_item_url(self):
        return self.avito_driver.driver.current_url

    async def get_seller_name(self, driver):
        try:
            username = driver.find_element(
                "xpath", "//div[@data-marker='seller-info/name']"
            )
            return str(username.text)
        except NoSuchElementException as ex:
            logger.debug(f"No such element. {ex} ")
            return "Пользователь"

    async def get_title(self, driver):
        try:
            title = driver.find_element(
                "xpath", "//span[@data-marker='item-view/title-info']"
            )
            return str(title.text)
        except NoSuchElementException as ex:
            logger.debug(f"No such element. {ex} ")
            return "Продукт"

    async def get_location(self, driver):
        try:
            title = driver.find_element("xpath", "//div[@itemprop='address']")
            return str(title.text)
        except Exception as ex:
            logger.debug(ex)
            return "Неопределённая локация"

    async def get_price(self, driver):
        try:
            title = driver.find_element(
                "xpath", "//span[@data-marker='item-view/item-price']"
            )
            return str(title.text)
        except NoSuchElementException as ex:
            logger.debug(f"No such element. {ex} ")
            return "Договорная"

    async def get_category(self, driver):
        try:
            title = driver.find_elements("xpath", "//span[@itemprop='name']")
            return title[2].text if title[2].text == "..." else title[3].text
        except IndexError as ex:
            logger.debug(ex)
            return "Категория не распознана"

    async def get_created_at(self, driver):
        try:
            date = driver.find_element(
                "xpath", "//span[@data-marker='item-view/item-date']"
            )
            return str(date.text).replace("· ", "")
        except IndexError as ex:
            logger.debug(ex)
            return "Недавно"

    async def get_number_of_views(self, driver):
        try:
            views = driver.find_element(
                "xpath", "//span[@data-marker='item-view/total-views']"
            )
            return views.text
        except Exception as ex:
            logger.debug(ex)
            return "Неопределённое число просмотров "

    async def get_description(self, driver):
        desc = driver.find_element('xpath', "//div[@data-marker='item-view/item-description']")
        return desc.text

    async def get_data(self, items, fields_to_parse, limit=None):
        try:
            items = await items
            counter = 0  # Initialize a counter

            for item in items:
                if limit is not None and counter >= limit:
                    break  # Exit the loop if the limit is reached

                item.click()

                self.avito_driver.driver.switch_to.window(
                    self.avito_driver.driver.window_handles[1]
                )

                item_data = AvitoFields(
                    item_url=await self.get_item_url()
                    if "item_url" in fields_to_parse
                    else None,
                    user_name=await self.get_seller_name(self.avito_driver.driver)
                    if "user_name" in fields_to_parse
                    else None,
                    item_title=await self.get_title(self.avito_driver.driver)
                    if "item_title" in fields_to_parse
                    else None,
                    price=await self.get_price(self.avito_driver.driver)
                    if "price" in fields_to_parse
                    else None,
                    location=await self.get_location(self.avito_driver.driver)
                    if "location" in fields_to_parse
                    else None,
                    category=await self.get_category(self.avito_driver.driver)
                    if "category" in fields_to_parse
                    else None,
                    created_at=await self.get_created_at(self.avito_driver.driver)
                    if "created_at" in fields_to_parse
                    else None,
                    number_of_views=await self.get_number_of_views(
                        self.avito_driver.driver
                    )
                    if "number_of_views" in fields_to_parse
                    else None,
                    description=await self.get_description(self.avito_driver.driver)
                    if "description" in fields_to_parse
                    else None,
                )

                self.all_data.append(item_data)
                self.avito_driver.driver.close()
                self.avito_driver.driver.switch_to.window(
                    self.avito_driver.driver.window_handles[0]
                )

                counter += 1  # Increment the counter

        except Exception as ex:
            logger.exception(f"No data uploaded: {ex} ]")

    async def get_all_data(self, fields: List[str], region, category, limit=None) -> list:
        await self.get_data(self.get_items(region, category), fields, limit)
        filtered_data = [data.dict() for data in self.all_data]
        return filtered_data
