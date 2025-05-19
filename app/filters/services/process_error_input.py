from utils import t


import logging
from asyncio import sleep


async def process_error_input(msg, locale, e):
    logging.error(e)
    await msg.delete()
    delete = await msg.answer(t("incorrect_min_year_input", locale))
    await sleep(5)
    await delete.delete()