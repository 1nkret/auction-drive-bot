from app.filters.cb_data import FilterCBD
from app.filters.services.update_state_data_and_editing_message import update_state_data_and_editing_message
from app.filters.states import EditStates
from core.enums import EditSearchSettingsAction
from core.schemas.search_settings import SearchSettingsSchema
from utils import t


from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message


router = Router(name="edit_mark")


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.mark))
async def edit_filter_mark(cb: CallbackQuery, state: FSMContext, locale: str):
    """Edit mark field"""
    await state.set_state(EditStates.edit_mark)
    await cb.message.edit_text(text=t("edit_mark", locale))


@router.message(EditStates.edit_mark)
async def edit_filter_mark_input(msg: Message, state: FSMContext, locale: str):
    """Saves mark in filter`s settings"""
    data = await state.get_data()
    settings = SearchSettingsSchema(**data.get("settings", {}))
    user_input = msg.text.strip().lower()
    if user_input == "0":
        settings.mark = None
    else:
        settings.mark = user_input

    await update_state_data_and_editing_message(msg, state, locale, data, settings)
