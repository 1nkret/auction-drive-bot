from app.filters.cb_data import FilterCBD
from app.filters.handlers.read_filter import read_filter
from core.enums import EditSearchSettingsAction, SearchSettingsAction
from core.models import SearchSettings
from core.schemas.search_settings import SearchSettingsSchema
from utils import get_user, t


from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


router = Router(name="save_filter")


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.done))
async def edit_filter_done(cb: CallbackQuery, state: FSMContext, session: AsyncSession, locale: str):
    """Save filter"""
    data = await state.get_data()
    settings = SearchSettingsSchema(**data.get("settings", {}))
    if not settings.mark:
        await cb.answer(text=t("mark_required", locale))
        return
    if not settings.model:
        await cb.answer(text=t("model_required", locale))
        return


    user = await get_user(session, cb.from_user.id)
    if settings.id:
        search_settings = (await session.execute(select(SearchSettings).filter(SearchSettings.id == settings.id))).scalar_one_or_none()
        for key, value in settings.model_dump(exclude_none=True).items():
            setattr(search_settings, key, value)
    else:
        search_settings = SearchSettings(
            user_id=user.id,
            **settings.model_dump(exclude_none=True)
        )

    session.add(search_settings)
    await session.commit()
    await session.refresh(search_settings)

    await state.clear()
    await cb.answer(text=t("filter_saved", locale))
    await read_filter(cb, FilterCBD(action=SearchSettingsAction.read, filter_id=search_settings.id), locale, state, session)