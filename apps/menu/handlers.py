from aiogram import types, Router
from aiogram.filters import Command
from utils.loader.locales import t

router = Router()


@router.message(Command("start"))
async def handle_menu(message: types.Message):
    await message.answer(t("start_message", message.from_user.language_code or "en"))
