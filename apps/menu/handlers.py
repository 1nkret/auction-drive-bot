from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from apps.filter.handlers import router
from apps.menu.services import register_user_if_not_exitst
from apps.keyboards.inline.main_menu import get_main_menu_kb
from core.middleware.database import DatabaseMiddleware
from utils import t


router = Router(name="menu")
router.message.middleware(DatabaseMiddleware())


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, locale: str):
    await register_user_if_not_exitst(message, session)

    await message.answer(
        text=t("start_message", locale=locale),
        reply_markup=get_main_menu_kb()
    )


@router.callback_query(F.data == "help")
async def cmd_help(cb: CallbackQuery, locale: str):
    await cb.message.edit_text(
        text=t("help_message", locale=locale),
        reply_markup=get_main_menu_kb()
    )


@router.callback_query(F.data == "about")
async def cmd_about(cb: CallbackQuery, locale: str):
    await cb.message.edit_text(
        text=t("about_message", locale=locale),
        reply_markup=get_main_menu_kb()
    )
