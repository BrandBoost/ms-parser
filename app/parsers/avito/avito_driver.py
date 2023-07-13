from selenium import webdriver

from app.config import settings


class AvitoDriver:
    def __init__(self):
        self.driver = None

    def create_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument(settings.USER_AGENT)
        options.add_argument(settings.AUTOMATION_CONTROLLED)
        options.add_argument(settings.GOOGLE_CHROME_BIN)
        options.add_argument("--headless")
        options.add_argument("disable-dev-shm-usage")
        options.binary_location = settings.CHROMEDRIVER_PATH

        return options

    async def initialize(self):
        options = self.create_options()
        self.driver = webdriver.Chrome(options=options)

    async def close_page(self):
        if self.driver:
            self.driver.close()

    async def quit(self):
        if self.driver:
            self.driver.quit()
