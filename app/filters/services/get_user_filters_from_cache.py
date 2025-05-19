from app.filters.services.setup_filter_settings_for_editing import setup_filter_settings_for_editing
from core.models import SearchSettings, User
from utils import t


from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


async def get_user_filters_from_cache(cb: CallbackQuery, locale: str, state: FSMContext, session: AsyncSession) -> list[SearchSettings]:
    data = await state.get_data()
    user_filters: list[SearchSettings] = data.get("user_filters")
    if not user_filters:
        user_filters = (await session.execute(select(SearchSettings).options(selectinload(SearchSettings.user)).filter(User.telegram_id == cb.from_user.id).order_by(SearchSettings.id))).scalars().all()
        if not user_filters:
            cb.answer(t("no_filters_create_new", locale))
            return await setup_filter_settings_for_editing(callback=cb, locale=locale, state=state)
        await state.update_data(user_filters=user_filters)
    return user_filters