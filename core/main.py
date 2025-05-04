import asyncio
import logging

from aiogram.exceptions import TelegramNetworkError
from core.config import dp, bot
from core.middleware.locale import LocaleMiddleware
from apps import menu, filter


async def start_bot():
    dp.include_routers(
        menu.router,
        filter.router
    )

    dp.message.middleware(LocaleMiddleware())
    dp.callback_query.middleware(LocaleMiddleware())

    tries = 0
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
        logging.info("Bot started successful.")
        tries = 0
    except TelegramNetworkError:
        tries += 1
        logging.info(f"Check your internet connection. Tries {tries}")
        await asyncio.sleep(tries)
