from app.filters.cb_data import FilterCBD
from app.filters.services.process_error_input import process_error_input
from app.filters.services.update_state_data_and_editing_message import update_state_data_and_editing_message
from app.filters.states import EditStates
from core.enums import DriveTypeEnum, EditSearchSettingsAction
from core.schemas.search_settings import SearchSettingsSchema
from utils import t


from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message


router = Router(name="edit_drive_type")


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.drive_type))
async def edit_filter_drive_type(cb: CallbackQuery, state: FSMContext, locale: str):
    """Edit drive_type field"""
    await state.set_state(EditStates.edit_drive_type)
    await cb.message.edit_text(text=t("edit_drive_type", locale))


@router.message(EditStates.edit_drive_type)
async def edit_filter_drive_type_input(msg: Message, state: FSMContext, locale: str):
    """Saves drive_type in filter`s settings"""
    try:
        data = await state.get_data()
        settings = SearchSettingsSchema(**data.get("settings", {}))
        user_input = msg.text.strip().lower()
        if user_input == "0":
            settings.drive_type = None
        else:
            drive_type = user_input
            if drive_type in DriveTypeEnum:
                settings.drive_type = drive_type
            else:
                raise ValueError("Incorrect drive type")

        await update_state_data_and_editing_message(msg, state, locale, data, settings)
    except ValueError as e:
        await process_error_input(msg, locale, e)
