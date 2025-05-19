from app.filters.cb_data import FilterCBD
from app.filters.services.setup_filter_settings_for_editing import setup_filter_settings_for_editing
from core.enums import SearchSettingsAction
from core.models import SearchSettings


from aiogram import F, Router
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


router = Router(name="setup_editing_filter")


@router.callback_query(or_f(FilterCBD.filter(F.action == SearchSettingsAction.create), FilterCBD.filter((F.action == SearchSettingsAction.edit) & (F.edit_action == None))))
async def setup_editing_filter(
    cb: CallbackQuery,
    callback_data: FilterCBD,
    session: AsyncSession,
    state: FSMContext,
    locale: str,
    ):
    """Create new filter"""
    filt_obj = None
    if callback_data.action == SearchSettingsAction.edit:
        filt_obj = (await session.execute(select(SearchSettings).filter(SearchSettings.id == callback_data.filter_id))).scalar_one_or_none()
    await setup_filter_settings_for_editing(callback=cb, locale=locale, state=state, filt_obj=filt_obj)