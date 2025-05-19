from app.filters.cb_data import FilterCBD
from app.filters.services.process_error_input import process_error_input
from app.filters.services.update_state_data_and_editing_message import update_state_data_and_editing_message
from core.enums import EditSearchSettingsAction
from core.schemas.search_settings import SearchSettingsSchema


from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


router = Router(name="edit_allow_damaged")


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.allow_damaged))
async def edit_filter_allow_damaged(cb: CallbackQuery, state: FSMContext, locale: str):
    """Edit allow_damaged field"""
    data = await state.get_data()
    settings = SearchSettingsSchema(**data.get("settings", {}))
    try:
        settings.allow_damaged = not settings.allow_damaged

        await update_state_data_and_editing_message(cb.message, state, locale, data, settings)
    except Exception as e:
        await process_error_input(cb.message, locale, e)
