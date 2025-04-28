from aiogram import types, Router
from aiogram.filters import Command
from utils import t

router = Router()


@router.message(Command("search"))
async def message_search_handler(message: types.Message):
    await search_handler(message)


@router.callback_query(lambda d: d.data == "search")
async def callback_search_handler(query: types.CallbackQuery):
    await search_handler(query.message)


async def search_handler(event):
    await event.answer(t("search_message", event.from_user.language_code or "en"))
