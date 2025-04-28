from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_inline_kb(sizes: list, buttons: dict[str, str]):
    kb = InlineKeyboardBuilder()
    for text, data in buttons.items():
        kb.add(InlineKeyboardButton(text=text, callback_data=data))
    return kb.adjust(*sizes).as_markup()
