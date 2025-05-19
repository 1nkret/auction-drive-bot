from app.filters.cb_data import FilterCBD
from app.filters.services.get_msg_and_kb_user_filter import get_msg_and_kb_user_filter
from app.filters.services.get_user_filters_from_cache import get_user_filters_from_cache
from core.enums import SearchSettingsAction
from core.models import SearchSettings


from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession


router = Router(name="read_filter")


@router.callback_query(FilterCBD.filter(F.action == SearchSettingsAction.read))
async def read_filter(cb: CallbackQuery, callback_data: FilterCBD, locale: str, state: FSMContext, session: AsyncSession):
    """Read filter"""
    user_filters = await get_user_filters_from_cache(cb, locale, state, session)
    if not callback_data.filter_id:
        show_filter: SearchSettings = user_filters[0]
    else:
        for i in user_filters:
            if i.id == callback_data.filter_id:
                show_filter = i
                break
    msg, kb = get_msg_and_kb_user_filter(user_filters, show_filter, locale)
    await cb.message.edit_text(text=msg, reply_markup=kb)