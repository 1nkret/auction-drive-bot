import asyncio
import logging

from aiogram.exceptions import TelegramNetworkError
from core.config import dp, bot
from utils.loader.router_loader import load_routers


async def start_bot():
    dp.include_routers(
        load_routers()
    )

    tries = 0
    try:
        await dp.start_polling(bot)
        logging.info("Bot started successful.")
        tries = 0
    except TelegramNetworkError:
        tries += 1
        logging.info(f"Check your internet connection. Tries {tries}")
        await asyncio.sleep(tries)
