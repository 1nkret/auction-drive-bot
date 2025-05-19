from app.filters.cb_data import FilterCBD
from app.filters.handlers.read_filter import read_filter
from app.filters.states import EditStates
from core.enums import SearchSettingsAction
from core.models import SearchSettings
from utils import build_inline_kb, t

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


router = Router(name="delete_filter")


@router.callback_query(FilterCBD.filter(F.action == SearchSettingsAction.delete))
async def delete_filter(cb: CallbackQuery, callback_data: FilterCBD, state: FSMContext, session: AsyncSession, locale: str):
    """Delete filter"""
    await state.update_data(delete_filter_id=callback_data.filter_id)
    await state.set_state(EditStates.confirm_delete)
    await cb.message.edit_text(
        text=t("confirm_delete_filter", locale),
        reply_markup=build_inline_kb(
            sizes=[1],
            buttons={
                t("yes", locale): "confirm_delete",
                t("no", locale): "cancel_delete"
            }
        )
    )


@router.callback_query(EditStates.confirm_delete)
async def confirm_delete_filter(cb: CallbackQuery, state: FSMContext, session: AsyncSession, locale: str):
    """Confirm delete filter"""
    data = await state.get_data()
    filter_id = data.get("delete_filter_id")
    if cb.data == "confirm_delete":
        await session.delete((await session.execute(select(SearchSettings).filter(SearchSettings.id == filter_id))).scalar_one_or_none())
        await session.commit()
        await cb.answer(text=t("filter_deleted", locale))
        await state.clear()
        await read_filter(cb, FilterCBD(action=SearchSettingsAction.read), locale, state, session)
    elif cb.data == "cancel_delete":
        del data["delete_filter_id"]
        await state.set_data(data)
        await cb.answer(text=t("delete_canceled", locale))
        await read_filter(cb, FilterCBD(action=SearchSettingsAction.read, filter_id=filter_id), locale, state, session)
