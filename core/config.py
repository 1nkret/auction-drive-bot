from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from os import getenv

load_dotenv()
API_TOKEN = getenv("API_TOKEN")
API_AUTORIA = getenv("API_AUTORIA")
owner_url = getenv("OWNER_TELEGRAM_URL")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
DEFAULT_LANGUAGE = "en"  # en/uk/ru

POSTGRES_DB = "postgres"
POSTGRES_USER = "your_username"
POSTGRES_PASSWORD = "your_password"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
