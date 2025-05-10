from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.models import SearchSettings, User
from core.middleware.database import DatabaseMiddleware
from apps.filter.cb_data import FilterCBD
from core.enums import SearchSettingsAction, EditSearchSettingsAction
from utils import get_user, build_inline_kb, t
from typing import Tuple, Optional
from pydantic import BaseModel

router = Router()
router.callback_query.middleware(DatabaseMiddleware())
router.message.middleware(DatabaseMiddleware())


class SearchSettingsSchema(BaseModel):
    mark: Optional[str] = None
    model: Optional[str] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None
    min_mileage: Optional[int] = None
    max_mileage: Optional[int] = None
    engine_type: Optional[str] = None
    drive_type: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    allow_damaged: Optional[bool] = None


class EditStates(StatesGroup):
    editing = State()
    edit_mark = State()
    edit_model = State()
    edit_min_year = State()
    edit_max_year = State()
    edit_min_mileage = State()
    edit_max_mileage = State()
    edit_engine_type = State()
    edit_drive_type = State()
    edit_min_price = State()
    edit_max_price = State()
    edit_allow_damaged = State()


@router.callback_query(FilterCBD.filter(F.action == SearchSettingsAction.read))
async def read_filter(cb: CallbackQuery, callback_data: FilterCBD, session: AsyncSession, locale: str, state: FSMContext):
    """Read filter"""
    if not callback_data.filter_id:
        return await create_new_search_settings(callback=cb, session=session, locale=locale, state=state)


@router.callback_query(FilterCBD.filter(F.action == SearchSettingsAction.create))
async def create_filter(
    cb: CallbackQuery, 
    state: FSMContext,
    session: AsyncSession, 
    locale: str,
    ):
    """Create new filter"""
    await create_new_search_settings(cb, session, locale, state)


async def create_new_search_settings(
    callback: CallbackQuery, 
    state: FSMContext, 
    session: AsyncSession, 
    locale: str
    ):
    settings_schema = SearchSettingsSchema()
    
    await state.set_state(EditStates.editing)
    await state.set_data({
        "settings": settings_schema.model_dump(),
        "edit_settings_msg": callback.message
    })
    
    msg_text, kb = show_edit_msg(locale, settings_schema)
    
    await callback.message.edit_text(text=msg_text, reply_markup=kb)


def show_edit_msg(locale: str, settings: SearchSettingsSchema) -> Tuple[str, InlineKeyboardMarkup]:
    kb = build_inline_kb(
        sizes=[2, 2, 2, 2, 2, 1, 1],
        buttons={
            t("kb_btn_mark", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.mark).pack(),
            t("kb_btn_model", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.model).pack(),
            t("kb_btn_min_year", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.min_year).pack(),
            t("kb_btn_max_year", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.max_year).pack(),
            t("kb_btn_min_mileage", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.min_mileage).pack(),
            t("kb_btn_max_mileage", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.max_mileage).pack(),
            t("kb_btn_engine", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.engine_type).pack(),
            t("kb_btn_drive", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.drive_type).pack(),
            t("kb_btn_min_price", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.min_price).pack(),
            t("kb_btn_max_price", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.max_price).pack(),
            t("kb_btn_damage", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.allow_damaged).pack(),
            t("kb_btn_done", locale): FilterCBD(action=SearchSettingsAction.edit, edit_action=EditSearchSettingsAction.done).pack(),
        }
    )
    
    return (t("select_param", locale), kb)


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.mark))
async def edit_filter_mark(cb: CallbackQuery, state: FSMContext, locale: str):
    """Edit mark field"""
    await state.set_state(EditStates.edit_mark)
    await cb.message.edit_text(text=t("edit_mark", locale))


@router.message(EditStates.edit_mark)
async def edit_filter_mark_input(msg: Message, state: FSMContext, locale: str):
    data = await state.get_data()
    settings = SearchSettingsSchema(**data.get("settings", {}))
    settings.mark = msg.text.strip().lower()
    
    await state.update_data(settings=settings.model_dump())
    
    msg_to_edit: Message = data.get("edit_settings_msg")
    text, kb = show_edit_msg(locale, settings)
    await msg.delete()
    await msg_to_edit.edit_text(text=text, reply_markup=kb)


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.done))
async def edit_filter_done(cb: CallbackQuery, state: FSMContext, session: AsyncSession, locale: str):
    """Save filter"""
    data = await state.get_data()
    settings = SearchSettingsSchema(**data.get("settings", {}))
    
    user = await get_user(session, cb.from_user.id)
    search_settings = SearchSettings(
        user_id=user.id,
        **settings.dict(exclude_none=True)
    )
    
    session.add(search_settings)
    await session.commit()
    
    await state.clear()
    await cb.message.edit_text(text=t("filter_saved", locale))


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.model))
async def edit_model_model(cb: CallbackQuery):
    """Edit model field"""


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.min_year))
async def edit_filter_min_year(cb: CallbackQuery):
    """Edit min_year field"""


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.max_year))
async def edit_filter_max_year(cb: CallbackQuery):
    """Edit max_year field"""


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.min_mileage))
async def edit_filter_min_mileage(cb: CallbackQuery):
    """Edit min_mileage field"""


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.max_mileage))
async def edit_filter_mark(cb: CallbackQuery):
    """Edit allow_damaged field"""


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.engine_type))
async def edit_filter_max_mileage(cb: CallbackQuery):
    """Edit max_mileage field"""


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.drive_type))
async def edit_filter_drive_type(cb: CallbackQuery):
    """Edit drive_type field"""


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.min_price))
async def edit_filter_min_price(cb: CallbackQuery):
    """Edit min_price field"""


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.max_price))
async def edit_filter_max_price(cb: CallbackQuery):
    """Edit max_price field"""


@router.callback_query(FilterCBD.filter(F.edit_action == EditSearchSettingsAction.allow_damaged))
async def edit_filter_allow_damaged(cb: CallbackQuery):
    """Edit allow_damaged field"""