from app.filters.cb_data import FilterCBD
from app.filters.services.update_state_data_and_editing_message import update_state_data_and_editing_message
from app.filters.states import EditStates
from core.enums import EditSearchSettingsAction
from core.schemas.search_settings import SearchSettingsSchema
from utils import t


from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message


router = Router(name="edit_model")


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.model))
async def edit_filter_model(cb: CallbackQuery, state: FSMContext, locale: str):
    """Edit model field"""
    await state.set_state(EditStates.edit_model)
    await cb.message.edit_text(text=t("edit_model", locale))


@router.message(EditStates.edit_model)
async def edit_filter_model_input(msg: Message, state: FSMContext, locale: str):
    """Saves model in filter`s settings"""
    data = await state.get_data()
    settings = SearchSettingsSchema(**data.get("settings", {}))
    user_input = msg.text.strip().lower()
    if user_input == "0":
        settings.model = None
    else:
        settings.model = user_input

    await update_state_data_and_editing_message(msg, state, locale, data, settings)