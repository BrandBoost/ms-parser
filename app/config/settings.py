import logging
import os

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger()
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s: %(levelname)s: %(message)s"
)

# FastAPI
HOST = os.getenv("FASTAPI_HOST", "0.0.0.0")
PORT = os.getenv("FASTAPI_PORT", "8000")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
AUTOMATION_CONTROLLED = os.getenv("AUTOMATION_CONTROLLED")

# Yandex
ORGANIZATIONS_API_KEY_YANDEX_KEY = os.getenv("ORGANIZATIONS_API_KEY_YANDEX_KEY")
GEOCODER_API_KEY_YANDEX_KEY = os.getenv("GEOCODER_API_KEY_YANDEX_KEY")
ORGANIZATION_URL = (
    f"https://search-maps.yandex.ru/v1/?apikey={ORGANIZATIONS_API_KEY_YANDEX_KEY}"
)
GEOCODER_URL = (
    f"https://geocode-maps.yandex.ru/1.x/?apikey={GEOCODER_API_KEY_YANDEX_KEY}"
)

# CORS
URL_LOCALHOST_FRONT = os.getenv("URL_LOCALHOST_FRONT")
URL_BRENDBOOST_BACK = os.getenv("URL_BRENDBOOST_BACK")
URL_BRENDBOOST_FRONT = os.getenv("URL_BRENDBOOST_FRONT")

# VK
VK_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# Avito
GOOGLE_CHROME_BIN = os.getenv("GOOGLE_CHROME_BIN")
CHROMEDRIVER_PATH = os.getenv("CROMDRIVER_PATH")

# MongoManager configuration
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Token configuration
SECRET_KEY = os.getenv('SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
JWT_ACCESS_TTL = int(os.environ.get('JWT_ACCESS_TTL', 50))
JWT_REFRESH_TTL = int(os.environ.get('JWT_REFRESH_TTL', 500))
REFRESH_TOKEN_JWT_SUBJECT = 'refresh'
ACCESS_TOKEN_JWT_SUBJECT = 'access'
TOKEN_TYPE = "Bearer"
