"""Create middleware for locale"""

from typing import Callable
from aiogram import BaseMiddleware
from aiogram.types import Message



class LocaleMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Message, data: dict):
        if event.from_user:
            data["locale"] = event.from_user.language_code
        return await handler(event, data)
