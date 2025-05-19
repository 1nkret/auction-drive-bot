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


router = Router(name="edit_max_price")


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.max_price))
async def edit_filter_max_price(cb: CallbackQuery, state: FSMContext, locale: str):
    """Edit max_price field"""
    await state.set_state(EditStates.edit_max_price)
    await cb.message.edit_text(text=t("edit_max_price", locale))


@router.message(EditStates.edit_max_price)
async def edit_filter_max_price_input(msg: Message, state: FSMContext, locale: str):
    """Saves max_price in filter`s settings"""
    data = await state.get_data()
    settings = SearchSettingsSchema(**data.get("settings", {}))
    try:
        user_input = msg.text.strip().lower()
        if user_input == "0":
            settings.max_price = None
        else:
            price = int(user_input)
            if price >= 0:
                min_price = (settings.min_price < price) if settings.min_price else True
                if min_price:
                    settings.max_price = price
                else:
                    raise Exception("Max price is less than min price")
            else:
                raise Exception("User input less than 0")

        await update_state_data_and_editing_message(msg, state, locale, data, settings)
    except Exception as e:
        await process_error_input(msg, locale, e)