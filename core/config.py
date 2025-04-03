from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from os import getenv

load_dotenv()
API_TOKEN = getenv("API_TOKEN")
owner_url = getenv("OWNER_TELEGRAM_URL")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
