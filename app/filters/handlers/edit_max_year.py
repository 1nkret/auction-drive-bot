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


router = Router(name="edit_max_year")


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.max_year))
async def edit_filter_max_year(cb: CallbackQuery, state: FSMContext, locale: str):
    """Edit max_year field"""
    await state.set_state(EditStates.edit_max_year)
    await cb.message.edit_text(text=t("edit_max_year", locale))


@router.message(EditStates.edit_max_year)
async def edit_filter_max_year_input(msg: Message, state: FSMContext, locale: str):
    """Saves max_year in filter`s settings"""
    data = await state.get_data()
    settings = SearchSettingsSchema(**data.get("settings", {}))
    try:
        user_input = msg.text.strip().lower()
        if user_input == "0":
            settings.max_year = None
        else:
            year = int(user_input)
            if year > 0:
                min_year = (settings.min_year < year) if settings.min_year else True
                if min_year:
                    settings.max_year = year
                else:
                    raise Exception("Max year is less than min year")
            else:
                raise Exception("User input less than 0")

        await update_state_data_and_editing_message(msg, state, locale, data, settings)
    except Exception as e:
        await process_error_input(msg, locale, e)