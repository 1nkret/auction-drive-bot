from app.filters.cb_data import FilterCBD
from app.filters.services.process_error_input import process_error_input
from app.filters.services.update_state_data_and_editing_message import update_state_data_and_editing_message
from app.filters.states import EditStates
from core.enums import EditSearchSettingsAction
from core.schemas.search_settings import SearchSettingsSchema
from utils import t


from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message


router = Router(name="edit_max_mileage")


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.max_mileage))
async def edit_filter_max_mileage(cb: CallbackQuery, state: FSMContext, locale: str):
    """Edit max_mileage field"""
    await state.set_state(EditStates.edit_max_mileage)
    await cb.message.edit_text(text=t("edit_max_mileage", locale))


@router.message(EditStates.edit_max_mileage)
async def edit_filter_max_mileage_input(msg: Message, state: FSMContext, locale: str):
    """Saves max_mileage in filter`s settings"""
    data = await state.get_data()
    settings = SearchSettingsSchema(**data.get("settings", {}))
    try:
        user_input = msg.text.strip().lower()
        if user_input == "0":
            settings.max_mileage = None
        else:
            mileage = int(user_input)
            if mileage >= 0:
                min_mileage = (settings.min_mileage < mileage) if settings.min_mileage else True
                if min_mileage:
                    settings.max_mileage = mileage
                else:
                    raise Exception("Max mileage is less than min mileage")
            else:
                raise Exception("User input less than 0")

        await update_state_data_and_editing_message(msg, state, locale, data, settings)
    except Exception as e:
        await process_error_input(msg, locale, e)
