from app.filters.cb_data import FilterCBD
from core.enums import EditSearchSettingsAction, SearchSettingsAction
from core.schemas.search_settings import SearchSettingsSchema
from utils import build_inline_kb, t


from aiogram.types import InlineKeyboardMarkup


from typing import Tuple


def get_msg_and_kb_edit_msg(locale: str, settings: SearchSettingsSchema) -> Tuple[str, InlineKeyboardMarkup]:
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
    msg_text = t("select_param", locale)
    msg_text = msg_text.format(
        mark=settings.mark or "...",
        model=settings.model or "...",
        min_year=settings.min_year or "...",
        max_year=settings.max_year or "...",
        min_mileage=settings.min_mileage or "...",
        max_mileage=settings.max_mileage or "...",
        engine_type=settings.engine_type or "...",
        drive_type=settings.drive_type or "...",
        min_price=settings.min_price or "...",
        max_price=settings.max_price or "...",
        allow_damaged="✅" if settings.allow_damaged else "🚫"
    )
    return (msg_text, kb)