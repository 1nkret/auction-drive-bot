from aiogram import types, Router
from aiogram.filters import CommandStart
from utils.loader.locales import t

router = Router()


@router.message(CommandStart())
async def handle_menu(message: types.Message):
    await message.answer(t("start_message", message.from_user.language_code or "en"))
