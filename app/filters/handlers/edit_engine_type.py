from app.filters.cb_data import FilterCBD
from app.filters.services.process_error_input import process_error_input
from app.filters.services.update_state_data_and_editing_message import update_state_data_and_editing_message
from app.filters.states import EditStates
from core.enums import EditSearchSettingsAction, EngineTypeEnum
from core.schemas.search_settings import SearchSettingsSchema
from utils import t


from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message


router = Router(name="edit_engine_type")


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.engine_type))
async def edit_filter_engine_type(cb: CallbackQuery, state: FSMContext, locale: str):
    """Edit engine_type field"""
    await state.set_state(EditStates.edit_engine_type)
    await cb.message.edit_text(text=t("edit_engine_type", locale))


@router.message(EditStates.edit_engine_type)
async def edit_filter_engine_type_input(msg: Message, state: FSMContext, locale: str):
    """Saves engine_type in filter`s settings"""
    try:
        data = await state.get_data()
        settings = SearchSettingsSchema(**data.get("settings", {}))
        user_input = msg.text.strip().lower()
        if user_input == "0":
            settings.engine_type = None
        else:
            engine_type = user_input
            if engine_type in EngineTypeEnum:
                settings.engine_type = engine_type
            else:
                raise ValueError("Incorrect engine type")

        await update_state_data_and_editing_message(msg, state, locale, data, settings)
    except ValueError as e:
        await process_error_input(msg, locale, e)
