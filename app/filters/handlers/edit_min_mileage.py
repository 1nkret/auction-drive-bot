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


router = Router(name="edit_min_mileage")


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.min_mileage))
async def edit_filter_min_mileage(cb: CallbackQuery, state: FSMContext, locale: str):
    """Edit min_mileage field"""
    await state.set_state(EditStates.edit_min_mileage)
    await cb.message.edit_text(text=t("edit_min_mileage", locale))


@router.message(EditStates.edit_min_mileage)
async def edit_filter_min_mileage_input(msg: Message, state: FSMContext, locale: str):
    """Saves min_milage in filter`s settings"""
    data = await state.get_data()
    settings = SearchSettingsSchema(**data.get("settings", {}))
    try:
        user_input = msg.text.strip().lower()
        if user_input == "0":
            settings.min_mileage = None
        else:
            mileage = int(user_input)
            if mileage >= 0:
                max_mileage = (settings.max_mileage > mileage) if settings.max_mileage else True
                if max_mileage:
                    settings.min_mileage = mileage
                else:
                    raise Exception("Min mileage is greater than max mileage")
            else:
                raise Exception("User input less than 0")

        await update_state_data_and_editing_message(msg, state, locale, data, settings)
    except Exception as e:
        await process_error_input(msg, locale, e)